class SocialFeatures {
    constructor() {
        this.likeButton = document.querySelector('.like-button');
        this.likeCount = document.querySelector('.like-count');
        this.shareButtons = document.querySelectorAll('.share-button');
        this.commentLikes = new Map();
        
        this.init();
    }

    init() {
        if (this.likeButton) {
            this.likeButton.addEventListener('click', () => this.handleArticleLike());
        }

        this.shareButtons.forEach(button => {
            button.addEventListener('click', (e) => this.handleShare(e));
        });

        this.loadLikes();
    }

    handleArticleLike() {
        const isLiked = this.likeButton.classList.contains('liked');
        const currentCount = parseInt(this.likeCount.textContent) || 0;
        
        if (isLiked) {
            this.likeButton.classList.remove('liked');
            this.likeCount.textContent = currentCount - 1;
        } else {
            this.likeButton.classList.add('liked');
            this.likeCount.textContent = currentCount + 1;
        }

        this.saveLikes();
    }

    handleCommentLike(commentId) {
        const comment = document.querySelector(`.comment[data-id="${commentId}"]`);
        const likeAction = comment.querySelector('.comment-action');
        const likeCount = comment.querySelector('.comment-like-count');
        
        const isLiked = this.commentLikes.get(commentId) || false;
        const currentCount = parseInt(likeCount.textContent) || 0;

        if (isLiked) {
            likeAction.classList.remove('liked');
            likeCount.textContent = currentCount - 1;
            this.commentLikes.set(commentId, false);
        } else {
            likeAction.classList.add('liked');
            likeCount.textContent = currentCount + 1;
            this.commentLikes.set(commentId, true);
        }

        this.saveCommentLikes();
    }

    handleShare(e) {
        e.preventDefault();
        const platform = e.currentTarget.dataset.platform;
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        
        let shareUrl;
        switch (platform) {
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                break;
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`;
                break;
            case 'pinterest':
                shareUrl = `https://pinterest.com/pin/create/button/?url=${url}&description=${title}`;
                break;
        }

        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    }

    saveLikes() {
        const likes = {
            articleLiked: this.likeButton.classList.contains('liked'),
            likeCount: parseInt(this.likeCount.textContent) || 0
        };
        localStorage.setItem('articleLikes', JSON.stringify(likes));
    }

    loadLikes() {
        const savedLikes = localStorage.getItem('articleLikes');
        if (savedLikes) {
            const likes = JSON.parse(savedLikes);
            if (likes.articleLiked) {
                this.likeButton.classList.add('liked');
            }
            this.likeCount.textContent = likes.likeCount;
        }

        const savedCommentLikes = localStorage.getItem('commentLikes');
        if (savedCommentLikes) {
            this.commentLikes = new Map(JSON.parse(savedCommentLikes));
            this.updateCommentLikeUI();
        }
    }

    saveCommentLikes() {
        localStorage.setItem('commentLikes', JSON.stringify(Array.from(this.commentLikes.entries())));
    }

    updateCommentLikeUI() {
        this.commentLikes.forEach((isLiked, commentId) => {
            const comment = document.querySelector(`.comment[data-id="${commentId}"]`);
            if (comment) {
                const likeAction = comment.querySelector('.comment-action');
                if (isLiked) {
                    likeAction.classList.add('liked');
                }
            }
        });
    }
}

// Initialize social features when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.socialFeatures = new SocialFeatures();
}); 