// Comment System
class CommentSystem {
    constructor() {
        this.comments = [];
        this.form = document.getElementById('commentForm');
        this.commentsList = document.getElementById('commentsList');
        this.commentCount = document.querySelector('.comment-count');
        this.noComments = document.querySelector('.no-comments');
        
        this.init();
    }

    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            this.loadComments();
        }
    }

    handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.form);
        const comment = {
            id: Date.now(),
            name: formData.get('name'),
            email: formData.get('email'),
            content: formData.get('comment'),
            date: new Date().toLocaleDateString(),
            likes: 0,
            replies: [],
            liked: false
        };

        this.addComment(comment);
        this.form.reset();
    }

    addComment(comment) {
        this.comments.unshift(comment);
        this.saveComments();
        this.renderComments();
    }

    addReply(commentId, reply) {
        const comment = this.comments.find(c => c.id === commentId);
        if (comment) {
            reply.id = Date.now();
            reply.date = new Date().toLocaleDateString();
            reply.likes = 0;
            comment.replies.push(reply);
            this.saveComments();
            this.renderComments();
        }
    }

    renderComments() {
        if (this.comments.length === 0) {
            this.noComments.style.display = 'block';
            this.commentsList.innerHTML = '';
            this.updateCommentCount();
            return;
        }

        this.noComments.style.display = 'none';
        this.commentsList.innerHTML = this.comments.map(comment => this.renderComment(comment)).join('');
        this.updateCommentCount();
    }

    renderComment(comment) {
        return `
            <div class="comment" data-id="${comment.id}">
                <div class="comment-header">
                    <span class="comment-author">${this.escapeHtml(comment.name)}</span>
                    <span class="comment-date">${comment.date}</span>
                </div>
                <div class="comment-content">
                    ${this.escapeHtml(comment.content)}
                </div>
                <div class="comment-actions">
                    <button class="comment-action like-button ${comment.liked ? 'liked' : ''}">
                        <i class="fas fa-heart"></i>
                        <span class="comment-like-count">${comment.likes}</span>
                    </button>
                    <button class="comment-action reply-button" onclick="commentSystem.showReplyForm(${comment.id})">
                        <i class="fas fa-reply"></i> Reply
                    </button>
                </div>
                <div class="reply-section" id="replySection-${comment.id}" style="display: none;">
                    <form class="reply-form" onsubmit="commentSystem.handleReplySubmit(event, ${comment.id})">
                        <div class="form-group">
                            <label for="reply-name-${comment.id}">Name</label>
                            <input type="text" id="reply-name-${comment.id}" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="reply-email-${comment.id}">Email</label>
                            <input type="email" id="reply-email-${comment.id}" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="reply-content-${comment.id}">Your Reply</label>
                            <textarea id="reply-content-${comment.id}" name="content" required></textarea>
                        </div>
                        <button type="submit" class="submit-comment">Post Reply</button>
                    </form>
                </div>
                ${comment.replies.length > 0 ? this.renderReplies(comment.replies) : ''}
            </div>
        `;
    }

    renderReplies(replies) {
        return `
            <div class="replies">
                ${replies.map(reply => `
                    <div class="comment reply">
                        <div class="comment-header">
                            <span class="comment-author">${this.escapeHtml(reply.name)}</span>
                            <span class="comment-date">${reply.date}</span>
                        </div>
                        <div class="comment-content">
                            ${this.escapeHtml(reply.content)}
                        </div>
                        <div class="comment-actions">
                            <button class="comment-action like-button" onclick="commentSystem.handleCommentLike(${reply.id})">
                                <i class="fas fa-heart"></i>
                                <span class="comment-like-count">${reply.likes}</span>
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    handleCommentLike(commentId) {
        const comment = this.findComment(commentId);
        if (comment) {
            if (comment.liked) {
                comment.likes--;
                comment.liked = false;
            } else {
                comment.likes++;
                comment.liked = true;
            }
            this.saveComments();
            this.renderComments();
        }
    }

    findComment(commentId) {
        // Search in main comments
        let comment = this.comments.find(c => c.id === commentId);
        if (comment) return comment;

        // Search in replies
        for (const mainComment of this.comments) {
            const reply = mainComment.replies.find(r => r.id === commentId);
            if (reply) return reply;
        }

        return null;
    }

    showReplyForm(commentId) {
        const replySection = document.getElementById(`replySection-${commentId}`);
        if (replySection) {
            replySection.style.display = replySection.style.display === 'none' ? 'block' : 'none';
        }
    }

    handleReplySubmit(e, commentId) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const reply = {
            name: formData.get('name'),
            email: formData.get('email'),
            content: formData.get('content')
        };

        this.addReply(commentId, reply);
        form.reset();
    }

    updateCommentCount() {
        const totalComments = this.comments.reduce((acc, comment) => 
            acc + 1 + comment.replies.length, 0);
        this.commentCount.textContent = `${totalComments} comment${totalComments !== 1 ? 's' : ''}`;
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    saveComments() {
        const articleId = window.location.pathname;
        localStorage.setItem(`comments_${articleId}`, JSON.stringify(this.comments));
    }

    loadComments() {
        const articleId = window.location.pathname;
        const savedComments = localStorage.getItem(`comments_${articleId}`);
        if (savedComments) {
            this.comments = JSON.parse(savedComments);
            this.renderComments();
        }
    }
}

// Initialize comment system
const commentSystem = new CommentSystem();

document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('comment-form');
    const commentsContainer = document.getElementById('comments-container');
    const commentCount = document.getElementById('comment-count');

    // Load comments from localStorage
    let comments = JSON.parse(localStorage.getItem('comments')) || {};
    const currentPage = window.location.pathname;
    
    if (!comments[currentPage]) {
        comments[currentPage] = [];
    }

    // Display comments
    function displayComments() {
        const pageComments = comments[currentPage];
        commentCount.textContent = pageComments.length;
        
        if (pageComments.length === 0) {
            commentsContainer.innerHTML = '<p class="no-comments">No comments yet. Be the first to comment!</p>';
            return;
        }

        const html = pageComments.map((comment, index) => `
            <div class="comment" data-id="${index}">
                <div class="comment-header">
                    <span class="comment-author">${comment.author}</span>
                    <span class="comment-date">${comment.date}</span>
                </div>
                <div class="comment-content">${comment.content}</div>
                <div class="comment-actions">
                    <button class="like-button ${comment.liked ? 'liked' : ''}">
                        <i class="fas fa-heart"></i>
                        <span class="like-count">${comment.likes}</span>
                    </button>
                    <button class="reply-button" onclick="showReplyForm(${index})">
                        <i class="fas fa-reply"></i> Reply
                    </button>
                </div>
                ${comment.replies ? `
                    <div class="replies">
                        ${comment.replies.map(reply => `
                            <div class="reply">
                                <div class="reply-header">
                                    <span class="reply-author">${reply.author}</span>
                                    <span class="reply-date">${reply.date}</span>
                                </div>
                                <div class="reply-content">${reply.content}</div>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                <div class="reply-form" id="reply-form-${index}" style="display: none;">
                    <textarea placeholder="Write your reply..." required></textarea>
                    <button onclick="submitReply(${index})">Submit Reply</button>
                </div>
            </div>
        `).join('');

        commentsContainer.innerHTML = html;
    }

    // Handle comment submission
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const author = document.getElementById('comment-author').value;
            const content = document.getElementById('comment-content').value;
            
            if (!author || !content) {
                alert('Please fill in all fields');
                return;
            }

            const newComment = {
                author: author,
                content: content,
                date: new Date().toLocaleDateString(),
                likes: 0,
                liked: false
            };

            comments[currentPage].unshift(newComment);
            localStorage.setItem('comments', JSON.stringify(comments));
            
            displayComments();
            commentForm.reset();
        });
    }

    // Toggle like on a comment
    window.toggleLike = function(index) {
        const comment = comments[currentPage][index];
        const likeButton = document.querySelector(`.comment[data-id="${index}"] .like-button`);
        
        if (comment.liked) {
            comment.likes--;
            comment.liked = false;
            likeButton.classList.remove('liked');
        } else {
            comment.likes++;
            comment.liked = true;
            likeButton.classList.add('liked');
        }
        
        localStorage.setItem('comments', JSON.stringify(comments));
        displayComments();
    };

    // Show reply form
    window.showReplyForm = function(index) {
        const replyForm = document.getElementById(`reply-form-${index}`);
        replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
    };

    // Submit reply
    window.submitReply = function(index) {
        const replyForm = document.getElementById(`reply-form-${index}`);
        const replyContent = replyForm.querySelector('textarea').value;
        
        if (!replyContent) {
            alert('Please write a reply');
            return;
        }

        const reply = {
            author: 'Anonymous',
            content: replyContent,
            date: new Date().toLocaleDateString()
        };

        if (!comments[currentPage][index].replies) {
            comments[currentPage][index].replies = [];
        }

        comments[currentPage][index].replies.push(reply);
        localStorage.setItem('comments', JSON.stringify(comments));
        
        displayComments();
        replyForm.style.display = 'none';
    };

    // Initial display
    displayComments();
}); 