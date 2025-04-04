import json
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class MealPlanGenerator:
    def __init__(self):
        self.recipes = self._load_recipes()
        self.supplements = self._load_supplements()
        
    def _load_recipes(self):
        with open('data/recipes.json', 'r') as f:
            return json.load(f)
    
    def _load_supplements(self):
        with open('data/supplements.json', 'r') as f:
            return json.load(f)
    
    def calculate_daily_calories(self, weight, activity_level):
        # Base calories per pound based on activity level
        calories_per_pound = {
            'sedentary': 20,
            'moderate': 25,
            'active': 30,
            'very-active': 35
        }
        return weight * calories_per_pound[activity_level]
    
    def select_recipes(self, preferences, num_recipes):
        selected_recipes = []
        for recipe in self.recipes:
            if len(selected_recipes) >= num_recipes:
                break
            if any(protein in recipe['proteins'] for protein in preferences['proteins']):
                selected_recipes.append(recipe)
        return selected_recipes
    
    def generate_shopping_list(self, recipes):
        shopping_list = {}
        for recipe in recipes:
            for ingredient in recipe['ingredients']:
                if ingredient in shopping_list:
                    shopping_list[ingredient] += 1
                else:
                    shopping_list[ingredient] = 1
        return shopping_list
    
    def create_pdf(self, cat_info, meal_plan, shopping_list, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            textColor=colors.HexColor('#34495e')
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        )
        
        # Header with logo
        header = Table([
            ['Cat Care Guide - Personalized Meal Plan'],
            [f'Generated on {datetime.now().strftime("%B %d, %Y")}']
        ])
        header.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, 1), 12),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#7f8c8d')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
        ]))
        elements.append(header)
        elements.append(Spacer(1, 20))
        
        # Cat Information Section
        elements.append(Paragraph("Cat Information", heading_style))
        cat_info_text = f"""
        <b>Name:</b> {cat_info['name']}<br/>
        <b>Age:</b> {cat_info['age']} years<br/>
        <b>Weight:</b> {cat_info['weight']} lbs<br/>
        <b>Activity Level:</b> {cat_info['activity_level'].replace('-', ' ').title()}<br/>
        <b>Daily Calorie Needs:</b> {meal_plan['daily_calories']} calories
        """
        elements.append(Paragraph(cat_info_text, normal_style))
        elements.append(Spacer(1, 20))
        
        # Meal Schedule Section
        elements.append(Paragraph("Daily Meal Schedule", heading_style))
        schedule_data = [['Time', 'Meal', 'Calories', 'Portion Size']]
        for meal in meal_plan['schedule']:
            schedule_data.append([
                meal['time'],
                meal['name'],
                f"{meal['calories']} cal",
                f"{meal['calories']/meal_plan['daily_calories']*100:.1f}%"
            ])
        
        schedule_table = Table(schedule_data)
        schedule_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e9ecef')),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(schedule_table)
        elements.append(Spacer(1, 20))
        
        # Recipes Section
        elements.append(Paragraph("Recipes", heading_style))
        for recipe in meal_plan['recipes']:
            elements.append(Paragraph(f"<b>{recipe['name']}</b>", normal_style))
            
            # Recipe details
            details = Table([
                ['Prep Time', 'Cook Time', 'Servings'],
                [recipe['prep_time'], recipe['cook_time'], recipe['servings']]
            ])
            details.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, 1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e9ecef')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(details)
            elements.append(Spacer(1, 10))
            
            # Ingredients
        # Shopping List
        elements.append(Paragraph("Shopping List", styles['Heading2']))
        shopping_data = [['Ingredient', 'Quantity']]
        for ingredient, quantity in shopping_list.items():
            shopping_data.append([ingredient, f"{quantity} units"])
        
        shopping_table = Table(shopping_data)
        shopping_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(shopping_table)
        
        # Build PDF
        doc.build(elements)
    
    def send_email(self, to_email, pdf_path, cat_name):
        # Email configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = f"Your Cat's Personalized Meal Plan - {cat_name}"
        msg['From'] = smtp_username
        msg['To'] = to_email
        
        # Email body
        body = f"""
        Dear Cat Parent,
        
        Thank you for using our meal planner! Please find attached your personalized meal plan for {cat_name}.
        
        This plan includes:
        - Daily calorie requirements
        - Meal schedule
        - Recipe collection
        - Shopping list
        
        If you have any questions about the meal plan, please don't hesitate to contact us.
        
        Best regards,
        Cat Care Guide Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        with open(pdf_path, 'rb') as f:
            pdf = MIMEApplication(f.read(), _subtype='pdf')
            pdf.add_header('Content-Disposition', 'attachment', filename=f'meal_plan_{cat_name.lower().replace(" ", "_")}.pdf')
            msg.attach(pdf)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    
    def generate_plan(self, form_data):
        # Calculate daily calories
        daily_calories = self.calculate_daily_calories(
            float(form_data['cat-weight']),
            form_data['activity-level']
        )
        
        # Select recipes based on preferences
        selected_recipes = self.select_recipes(
            {'proteins': form_data.getlist('protein')},
            int(form_data['preferred-recipes'])
        )
        
        # Generate meal schedule
        schedule = []
        meals_per_day = 3
        calories_per_meal = daily_calories / meals_per_day
        
        for i in range(meals_per_day):
            recipe = selected_recipes[i % len(selected_recipes)]
            schedule.append({
                'time': f"{8 + i*6}:00",
                'name': recipe['name'],
                'calories': round(calories_per_meal)
            })
        
        # Generate shopping list
        shopping_list = self.generate_shopping_list(selected_recipes)
        
        # Create meal plan object
        meal_plan = {
            'daily_calories': round(daily_calories),
            'schedule': schedule,
            'recipes': selected_recipes,
            'shopping_list': shopping_list
        }
        
        # Create cat info object
        cat_info = {
            'name': form_data['cat-name'],
            'age': form_data['cat-age'],
            'weight': form_data['cat-weight'],
            'activity_level': form_data['activity-level']
        }
        
        # Generate PDF
        pdf_filename = f"meal_plan_{cat_info['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf_path = os.path.join('generated_plans', pdf_filename)
        os.makedirs('generated_plans', exist_ok=True)
        self.create_pdf(cat_info, meal_plan, shopping_list, pdf_path)
        
        # Send email
        self.send_email(form_data['email'], pdf_path, cat_info['name'])
        
        return {
            'success': True,
            'message': 'Meal plan generated and sent successfully!',
            'pdf_path': pdf_path
        } 