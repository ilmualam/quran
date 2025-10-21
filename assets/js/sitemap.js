/**
 * @copyright    Copyright (C) 2025 - 2026 TheBukitBesi. All rights reserved.
 * @author       (https://ilmualam.com)
 * @version      1.2.0
 * @license      All Rights Reserved
 * This source file is proprietary and confidential. Unauthorized copying,
 * modification, distribution, or use of this file, via any medium, is
 * strictly prohibited without the express written permission of the author.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 _____________________________________________________________________________
 * Blogger Categorized Sitemap with Enhanced Thumbnails
 * Ultra-lightweight, SEO Optimized with Rich Schema.org
 * 5-column desktop grid, larger thumbnails, mobile optimized
 * Version 3.0 - Copyrighted by ilmualam.com
 */
(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        blogUrl: 'https://www.ilmualam.com',
        postsPerLabel: 10,
        imageSize: 400,
        defaultThumb: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"%3E%3Crect width="400" height="300" fill="%23f0f0f0"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23999" font-family="sans-serif" font-size="16"%3ENo Image%3C/text%3E%3C/svg%3E',
        maxLabels: 25,
        excerptLength: 150,
        cacheExpiry: 3600000 // 1 hour cache
    };

    const cache = {
        labels: [],
        posts: {},
        currentLabel: null,
        timestamp: {}
    };

    function init() {
        const container = document.getElementById('recentpostsae');
        const navContainer = document.getElementById('recentpostnavfeed');

        if (!container || !navContainer) {
            console.error('Required containers not found: #recentpostsae or #recentpostnavfeed');
            return;
        }

        injectBaseStyles();
        loadLabels();
    }

    function injectBaseStyles() {
        if (document.getElementById('sitemap-styles')) return;

        const style = document.createElement('style');
        style.id = 'sitemap-styles';
        style.textContent = `
            /* CSS Isolation */
            #recentpostsae, #recentpostnavfeed {
                all: initial;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            }
            #recentpostsae *, #recentpostnavfeed * {
                all: revert;
            }

            /* Label Navigation */
            #recentpostnavfeed .label-nav {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin-bottom: 30px;
                justify-content: center;
                padding: 0 15px;
            }
            #recentpostnavfeed .label-btn {
                background: #fff;
                border: 2px solid #e0e0e0;
                padding: 10px 20px;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-size: 14px;
                font-weight: 500;
                text-decoration: none;
                color: #333;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                position: relative;
                overflow: hidden;
            }
            #recentpostnavfeed .label-btn::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                background: rgba(0,0,0,0.05);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }
            #recentpostnavfeed .label-btn:hover::before {
                width: 100%;
                height: 100%;
            }
            #recentpostnavfeed .label-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.12);
                border-color: #333;
            }
            #recentpostnavfeed .label-btn.active {
                background: #333;
                color: #fff;
                border-color: #333;
                font-weight: 600;
            }
            #recentpostnavfeed .all-posts-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                border: none;
            }
            #recentpostnavfeed .all-posts-btn:hover {
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            }

            /* Header */
            #recentpostsae .sitemap-header {
                text-align: center;
                margin: 30px 0;
                font-size: 32px;
                color: #2c3e50;
                font-weight: 700;
                position: relative;
                padding-bottom: 15px;
            }
            #recentpostsae .sitemap-header::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 80px;
                height: 4px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 2px;
            }

            /* Posts Grid */
            #recentpostsae .posts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin: 30px auto;
                padding: 0 10px;
                width: 100%;
                max-width: 100%;
            }

            /* Post Card */
            #recentpostsae .recentpost {
                background: #fff;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                display: flex;
                flex-direction: column;
                height: 100%;
                position: relative;
            }
            #recentpostsae .recentpost::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                transform: scaleX(0);
                transition: transform 0.3s;
            }
            #recentpostsae .recentpost:hover::before {
                transform: scaleX(1);
            }
            #recentpostsae .recentpost:hover {
                transform: translateY(-10px);
                box-shadow: 0 12px 35px rgba(0,0,0,0.15);
            }

            /* Thumbnail */
            #recentpostsae .post-thumb {
                width: 100%;
                height: 250px;
                object-fit: cover;
                background: #f5f5f5;
                display: block;
                transition: transform 0.5s;
            }
            #recentpostsae .recentpost:hover .post-thumb {
                transform: scale(1.05);
            }

            /* Content */
            #recentpostsae .post-content {
                padding: 20px;
                flex-grow: 1;
                display: flex;
                flex-direction: column;
            }
            #recentpostsae .post-title {
                font-size: 17px;
                font-weight: 600;
                margin: 0 0 12px 0;
                line-height: 1.4;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                min-height: 48px;
            }
            #recentpostsae .post-title a {
                color: #2c3e50;
                text-decoration: none;
                transition: color 0.3s;
            }
            #recentpostsae .post-title a:hover {
                color: #667eea;
            }
            #recentpostsae .post-excerpt {
                color: #6c757d;
                font-size: 14px;
                line-height: 1.6;
                flex-grow: 1;
                margin-bottom: 15px;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }
            #recentpostsae .post-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-top: 15px;
                border-top: 1px solid #f0f0f0;
                font-size: 13px;
                color: #95a5a6;
            }
            #recentpostsae .post-date {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            #recentpostsae .post-date::before {
                content: '📅';
                font-size: 14px;
            }
            #recentpostsae .read-more {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            #recentpostsae .read-more:hover {
                color: #764ba2;
                gap: 8px;
            }

            /* Loading Animation */
            #recentpostsae .loading-container {
                text-align: center;
                padding: 80px 20px;
            }
            #recentpostsae .loading-spinner {
                display: inline-block;
                width: 60px;
                height: 60px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            /* Responsive Design */
             @media (max-width: 1200px) {
                #recentpostsae .posts-grid {
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                }
            }
            @media (max-width: 992px) {
                #recentpostsae .posts-grid {
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                }
                #recentpostsae .sitemap-header {
                    font-size: 28px;
                }
            }
            @media (max-width: 768px) {
                #recentpostsae .posts-grid {
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                }
                #recentpostsae .post-thumb {
                    height: 200px;
                }
            }
            @media (max-width: 480px) {
                #recentpostsae .posts-grid {
                    grid-template-columns: 1fr;
                }
                #recentpostsae .sitemap-header {
                    font-size: 24px;
                }
                #recentpostnavfeed .label-nav {
                    gap: 8px;
                }
                #recentpostnavfeed .label-btn {
                    padding: 8px 16px;
                    font-size: 13px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    function loadLabels() {
        showLoading();
        const script = document.createElement('script');
        script.src = `${CONFIG.blogUrl}/feeds/posts/summary?alt=json-in-script&max-results=150&callback=BloggerSitemap.processLabels`;
        script.onerror = () => {
            console.error('Failed to load labels');
            showError('Failed to load categories. Please refresh the page.');
        };
        document.head.appendChild(script);
    }

    function processLabels(data) {
        const labelCount = new Map();
        if (data.feed.entry) {
            data.feed.entry.forEach(entry => {
                if (entry.category) {
                    entry.category.forEach(cat => {
                        const count = labelCount.get(cat.term) || 0;
                        labelCount.set(cat.term, count + 1);
                    });
                }
            });
        }

        cache.labels = Array.from(labelCount.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, CONFIG.maxLabels)
            .map(([label]) => label);

        displayLabelNav();

        if (cache.labels.length > 0) {
            loadLabelPosts(cache.labels[0]);
        } else {
            loadRecentPosts();
        }
    }

    function displayLabelNav() {
        const navContainer = document.getElementById('recentpostnavfeed');
        navContainer.innerHTML = '';

        const nav = document.createElement('nav');
        nav.className = 'label-nav';
        nav.setAttribute('role', 'navigation');
        nav.setAttribute('aria-label', 'Category Navigation');

        const allBtn = createLabelButton('📋 Semua Post', () => {
            setActiveButton(allBtn);
            loadRecentPosts();
        }, 'label-btn all-posts-btn');
        nav.appendChild(allBtn);

        cache.labels.forEach(label => {
            const btn = createLabelButton(
                getEmojiForLabel(label) + ' ' + label,
                () => {
                    setActiveButton(btn);
                    loadLabelPosts(label);
                }
            );
            nav.appendChild(btn);
        });

        navContainer.appendChild(nav);
    }

    function createLabelButton(text, onClick, className = 'label-btn') {
        const btn = document.createElement('button');
        btn.className = className;
        btn.textContent = text;
        btn.onclick = onClick;
        btn.setAttribute('aria-label', `View posts in ${text}`);
        return btn;
    }

    function setActiveButton(activeBtn) {
        document.querySelectorAll('#recentpostnavfeed .label-btn').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-pressed', 'false');
        });
        activeBtn.classList.add('active');
        activeBtn.setAttribute('aria-pressed', 'true');
    }

    function getEmojiForLabel(label) {
        const emojiMap = {
            'Islamik': '🕌', 'Doa': '🤲🏻', 'Al-Quran': '📖', 'Motivasi': 'ﷺ', 'Surah': '📄', 'Zikir': '📿', 'Qasidah': '👨🏼‍💻', 'Hukum': '🕋', 'Inspirasi': '💡', 'Ramadan': '✨', 'Waktu Solat': '🕗', 'Solat': '🛐', 'Panduan': '📝', 'Kisah Nabi': '🏜️', 'Feqah': '🍳', 'Akhlak': '👳‍♂️', 'Fardhu Ain': '📚', 'Iqra': '📜', 'Mari Mengaji': '📕',
        };
        const lowerLabel = label.toLowerCase();
        if (emojiMap[lowerLabel]) return emojiMap[lowerLabel];
        for (const [key, emoji] of Object.entries(emojiMap)) {
            if (lowerLabel.includes(key) || key.includes(lowerLabel)) {
                return emoji;
            }
        }
        return '📝';
    }

    function loadLabelPosts(label) {
        showLoading();
        cache.currentLabel = label;
        if (cache.posts[label] && isCacheValid(label)) {
            displayPosts(cache.posts[label], label);
            return;
        }
        const script = document.createElement('script');
        script.src = `${CONFIG.blogUrl}/feeds/posts/default/-/${encodeURIComponent(label)}?alt=json-in-script&max-results=${CONFIG.postsPerLabel}&callback=BloggerSitemap.processPosts`;
        script.onerror = () => showError(`Failed to load posts for ${label}`);
        document.head.appendChild(script);
    }

    function loadRecentPosts() {
        showLoading();
        cache.currentLabel = 'recent';
        if (cache.posts['recent'] && isCacheValid('recent')) {
            displayPosts(cache.posts['recent'], 'Semua Post Terkini');
            return;
        }
        const script = document.createElement('script');
        script.src = `${CONFIG.blogUrl}/feeds/posts/default?alt=json-in-script&max-results=25&orderby=published&callback=BloggerSitemap.processPosts`;
        script.onerror = () => showError('Failed to load recent posts');
        document.head.appendChild(script);
    }

    function isCacheValid(key) {
        const timestamp = cache.timestamp[key];
        return timestamp && (Date.now() - timestamp < CONFIG.cacheExpiry);
    }

    function processPosts(data) {
        const posts = [];
        if (data.feed.entry) {
            data.feed.entry.forEach(entry => {
                const post = {
                    title: entry.title.$t,
                    url: entry.link.find(l => l.rel === 'alternate')?.href || '',
                    thumbnail: extractThumbnail(entry),
                    excerpt: extractExcerpt(entry),
                    published: new Date(entry.published.$t),
                    updated: new Date(entry.updated.$t),
                    author: entry.author?.[0]?.name?.$t || 'Admin',
                    labels: entry.category ? entry.category.map(c => c.term) : [],
                    commentsCount: entry.thr$total ? entry.thr$total.$t : '0'
                };
                posts.push(post);
            });
        }
        const cacheKey = cache.currentLabel === 'recent' ? 'recent' : cache.currentLabel;
        cache.posts[cacheKey] = posts;
        cache.timestamp[cacheKey] = Date.now();
        displayPosts(posts, cache.currentLabel === 'recent' ? 'Semua Post Terkini' : cache.currentLabel);
    }

    function extractThumbnail(entry) {
        if (entry.media$thumbnail) {
            return optimizeImageUrl(entry.media$thumbnail.url);
        }
        const content = entry.content?.$t || entry.summary?.$t || '';
        const patterns = [
            /<img[^>]+src=["']([^"']+)["']/i,
            /<img[^>]+data-src=["']([^"']+)["']/i,
            /\[img\]([^\[]+)\[\/img\]/i
        ];
        for (const pattern of patterns) {
            const match = content.match(pattern);
            if (match && match[1]) {
                return optimizeImageUrl(match[1]);
            }
        }
        const youtubeMatch = content.match(/(?:youtube\.com\/embed\/|youtu\.be\/)([^"&?\/\s]{11})/);
        if (youtubeMatch) {
            return `https://i.ytimg.com/vi/${youtubeMatch[1]}/hqdefault.jpg`;
        }
        return CONFIG.defaultThumb;
    }

    function optimizeImageUrl(url) {
        if (url.includes('blogspot.com') || url.includes('googleusercontent.com')) {
            return url.replace(/\/s\d+(-c)?(-[a-z]+)?\//, `/w${CONFIG.imageSize}-h${Math.round(CONFIG.imageSize * 0.75)}-c/`);
        }
        if (url.includes('imgur.com')) {
            return url.replace(/\.(jpg|jpeg|png|gif)$/i, `l.$1`);
        }
        return url;
    }

    function extractExcerpt(entry) {
        const content = entry.content?.$t || entry.summary?.$t || '';
        let text = content
            .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
            .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
            .replace(/<[^>]+>/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
        text = text.replace(/\[...\]|\.\.\./g, '');
        return text.length > CONFIG.excerptLength ? text.substring(0, CONFIG.excerptLength).trim() + '...' : text;
    }

    function displayPosts(posts, labelName) {
        const container = document.getElementById('recentpostsae');
        let html = `<h2 class="sitemap-header">${getEmojiForLabel(labelName)} ${labelName}</h2>`;
        html += '<div class="posts-grid">';
        posts.forEach((post, index) => {
            const date = formatDate(post.published);
            html += `
                <article class="recentpost" itemscope itemtype="https://schema.org/BlogPosting">
                    <meta itemprop="headline" content="${escapeHtml(post.title)}">
                    <meta itemprop="datePublished" content="${post.published.toISOString()}">
                    <meta itemprop="author" content="${post.author}">
                    <img class="post-thumb" src="${post.thumbnail}" alt="${escapeHtml(post.title)}" loading="${index < 5 ? 'eager' : 'lazy'}" onerror="this.src='${CONFIG.defaultThumb}'" itemprop="image">
                    <div class="post-content">
                        <h3 class="post-title">
                            <a href="${post.url}" rel="bookmark" itemprop="url" title="${escapeHtml(post.title)}">${escapeHtml(post.title)}</a>
                        </h3>
                        ${post.excerpt ? `<p class="post-excerpt" itemprop="description">${escapeHtml(post.excerpt)}</p>` : ''}
                        <div class="post-meta">
                            <time class="post-date" datetime="${post.published.toISOString()}">${date}</time>
                            <a href="${post.url}" class="read-more" aria-label="Read more about ${escapeHtml(post.title)}">
                                Read More →
                            </a>
                        </div>
                    </div>
                </article>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
        generateEnhancedSchema(posts, labelName);
        if ('IntersectionObserver' in window) {
            lazyLoadImages();
        }
    }

    function formatDate(date) {
        const months = ['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogos', 'Sep', 'Okt', 'Nov', 'Dis'];
        return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
    }

    function escapeHtml(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;', '/': '&#x2F;' };
        return text.replace(/[&<>"'/]/g, m => map[m]);
    }

    function showLoading() {
        const container = document.getElementById('recentpostsae');
        container.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p style="margin-top: 20px; color: #666;">Memuatkan kandungan...</p>
            </div>
        `;
    }

    function showError(message) {
        const container = document.getElementById('recentpostsae');
        container.innerHTML = `
            <div style="text-align: center; padding: 50px; color: #e74c3c;">
                <p style="font-size: 48px; margin-bottom: 20px;">⚠️</p>
                <p>${message}</p>
                <button onclick="BloggerSitemap.init()" style="margin-top: 20px; padding: 10px 20px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Cuba Semula
                </button>
            </div>
        `;
    }

    function generateEnhancedSchema(posts, categoryName) {
        const schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "@id": window.location.href + "#collection",
                    "url": window.location.href,
                    "name": `${categoryName} - Ilmu Alam Blog`,
                    "description": `Koleksi artikel blog tentang ${categoryName} di Ilmu Alam Site`,
                    "isPartOf": { "@id": CONFIG.blogUrl + "#website" },
                    "hasPart": posts.map((post, index) => ({
                        "@type": "BlogPosting",
                        "@id": post.url + "#blogpost",
                        "position": index + 1
                    }))
                },
                {
                    "@type": "WebSite",
                    "@id": CONFIG.blogUrl + "#website",
                    "url": CONFIG.blogUrl,
                    "name": "Ilmu Alam",
                    "potentialAction": {
                        "@type": "SearchAction",
                        "target": CONFIG.blogUrl + "/search?q={search_term_string}",
                        "query-input": "required name=search_term_string"
                    }
                },
                ...posts.map((post, index) => ({
                    "@type": "BlogPosting",
                    "@id": post.url + "#blogpost",
                    "headline": post.title,
                    "url": post.url,
                    "mainEntityOfPage": { "@type": "WebPage", "@id": post.url },
                    "image": post.thumbnail !== CONFIG.defaultThumb ? {
                        "@type": "ImageObject",
                        "url": post.thumbnail,
                        "width": CONFIG.imageSize,
                        "height": Math.round(CONFIG.imageSize * 0.75)
                    } : undefined,
                    "datePublished": post.published.toISOString(),
                    "dateModified": post.updated.toISOString(),
                    "author": { "@type": "Person", "name": post.author },
                    "publisher": {
                        "@type": "Organization",
                        "name": "Ilmu Alam",
                        "logo": { "@type": "ImageObject", "url": CONFIG.blogUrl + "/logo.png" }
                    },
                    "description": post.excerpt,
                    "keywords": post.labels.join(", "),
                    "articleSection": categoryName,
                    "inLanguage": "ms-MY"
                }))
            ]
        };
        let scriptTag = document.getElementById('sitemap-schema');
        if (!scriptTag) {
            scriptTag = document.createElement('script');
            scriptTag.type = 'application/ld+json';
            scriptTag.id = 'sitemap-schema';
            document.head.appendChild(scriptTag);
        }
        scriptTag.textContent = JSON.stringify(schema);
    }

    function lazyLoadImages() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.src;
                    imageObserver.unobserve(img);
                }
            });
        }, { rootMargin: '50px 0px' });
        images.forEach(img => imageObserver.observe(img));
    }

    window.BloggerSitemap = {
        init: init,
        processLabels: processLabels,
        processPosts: processPosts,
        refresh: () => {
            Object.keys(cache.posts).forEach(key => delete cache.posts[key]);
            Object.keys(cache.timestamp).forEach(key => delete cache.timestamp[key]);
            init();
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
