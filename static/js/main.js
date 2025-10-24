document.addEventListener('DOMContentLoaded', function() {

    // --- YENİ: KAYDIRINCA DEĞİŞEN NAVBAR MANTIĞI ---
    const navbar = document.querySelector('.navbar.fixed-top');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) { // 50 piksel aşağı kaydırıldığında
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // --- TOAST BİLDİRİM FONKSİYONU ---
    function showToast(message, type = 'success') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;
        const toastId = 'toast-' + Date.now();
        const toastHTML = `
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="4000" id="${toastId}">
                <div class="toast-header">
                    <strong class="me-auto">AuraLuna</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">${message}</div>
            </div>`;
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const newToastEl = document.getElementById(toastId);
        const newToast = new bootstrap.Toast(newToastEl);
        newToast.show();
        newToastEl.addEventListener('hidden.bs.toast', () => newToastEl.remove());
    }

    // --- CSRF TOKEN YARDIMCI FONKSİYONU ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- AJAX FAVORİ MANTIĞI ---
    document.body.addEventListener('click', function(event) {
        const favouriteLink = event.target.closest('.js-toggle-favourite');
        if (favouriteLink) {
            event.preventDefault();
            const url = favouriteLink.href;
            const heartIcon = favouriteLink.querySelector('i');
            fetch(url, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    showToast(data.message);
                    if (data.is_favourited) { heartIcon.classList.remove('bi-heart'); heartIcon.classList.add('bi-heart-fill'); } 
                    else { heartIcon.classList.remove('bi-heart-fill'); heartIcon.classList.add('bi-heart'); }
                }
            })
            .catch(error => console.error('Favori işlemi sırasında hata:', error));
        }
    });

    // --- AJAX SEPET İŞLEMLERİ ---
    document.body.addEventListener('submit', function(event) {
        const cartForm = event.target.closest('.js-ajax-cart-form');
        if (cartForm) {
            event.preventDefault();
            const url = cartForm.action;
            const formData = new FormData(cartForm);
            fetch(url, {
                method: 'POST', body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    showToast(data.message);
                    const cartCounter = document.getElementById('cart-counter');
                    if (cartCounter) {
                        cartCounter.textContent = data.cart_total_items;
                        cartCounter.style.display = data.cart_total_items > 0 ? 'inline-block' : 'none';
                    }
                } else if (data.status === 'reload') {
                    showToast(data.message);
                    setTimeout(() => window.location.reload(), 1000);
                }
            })
            .catch(error => console.error('Sepet işlemi sırasında hata:', error));
        }
    });

    // --- ANA SAYFA KARUSELLERİ ---
    if (document.querySelector('.hero-swiper')) {
        new Swiper('.hero-swiper', { loop: true, autoplay: { delay: 5000, disableOnInteraction: false }, pagination: { el: '.swiper-pagination', clickable: true }, effect: 'fade', fadeEffect: { crossFade: true } });
    }
    if (document.querySelector('.product-swiper')) {
        new Swiper('.product-swiper', { slidesPerView: 1, spaceBetween: 10, breakpoints: { 576: { slidesPerView: 2, spaceBetween: 20 }, 768: { slidesPerView: 3, spaceBetween: 30 }, 992: { slidesPerView: 4, spaceBetween: 30 } }, navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' } });
    }

    // --- HIZLI BAKIŞ (QUICK VIEW) MODAL MANTIĞI ---
    const quickViewModalEl = document.getElementById('quickViewModal');
    if (quickViewModalEl) {
        const modalBody = quickViewModalEl.querySelector('.modal-body');
        quickViewModalEl.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget; const productSlug = button.dataset.slug;
            const url = `/products/quick-view/${productSlug}/`;
            modalBody.innerHTML = '<div class="d-flex justify-content-center align-items-center" style="min-height: 300px;"><div class="spinner-border" role="status"><span class="visually-hidden">Yükleniyor...</span></div></div>';
            fetch(url).then(response => response.json()).then(data => {
                modalBody.innerHTML = `<div class="row"><div class="col-md-6"><img src="${data.main_image ? data.main_image : '/static/images/placeholder.png'}" class="img-fluid rounded"></div><div class="col-md-6"><h3>${data.name}</h3><p class="text-muted">${data.category}</p><p>${data.description.substring(0, 150)}...</p><hr><a href="/products/p/${productSlug}/" class="btn btn-primary">Tüm Detayları Gör</a></div></div>`;
            }).catch(error => { modalBody.innerHTML = '<p class="text-danger">Ürün bilgileri yüklenirken bir hata oluştu.</p>'; console.error('Hızlı Bakış Hatası:', error); });
        });
    }

    // --- ÜRÜN DETAY SAYFASI MANTIĞI ---
    const variantsDataEl = document.getElementById('variants-data');
    if (variantsDataEl) {
        const variantsData = JSON.parse(variantsDataEl.textContent); const variants = variantsData;
        const mainImage = document.getElementById('main-product-image'); const thumbnails = document.querySelectorAll('.thumbnail-img');
        const colorSelector = document.getElementById('color-selector'); const sizeSelector = document.getElementById('size-selector');
        const priceDisplay = document.getElementById('product-price'); const stockDisplay = document.getElementById('product-stock');
        const addToCartBtn = document.getElementById('add-to-cart-btn'); const addToCartForm = document.getElementById('add-to-cart-form');
        const quantityInput = document.getElementById('quantity-input'); const quantityMinusBtn = document.getElementById('quantity-minus'); const quantityPlusBtn = document.getElementById('quantity-plus');
        let selectedColor = null, selectedSize = null, currentVariant = null;

        thumbnails.forEach(thumb => { thumb.addEventListener('click', function() { mainImage.src = this.src; thumbnails.forEach(t => t.classList.remove('active')); this.classList.add('active'); }); });
        const uniqueColors = [...new Set(variants.map(v => v.color))]; colorSelector.innerHTML = '';
        uniqueColors.forEach(color => { const colorDiv = document.createElement('div'); colorDiv.className = 'variant-swatch color-swatch'; colorDiv.textContent = color; colorDiv.dataset.color = color; colorSelector.appendChild(colorDiv); });
        colorSelector.querySelectorAll('.color-swatch').forEach(swatch => { swatch.addEventListener('click', function() { selectedColor = this.dataset.color; selectedSize = null; colorSelector.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected')); this.classList.add('selected'); updateSizeOptions(); resetDisplay(); }); });
        function updateSizeOptions() {
            sizeSelector.innerHTML = ''; const availableVariants = variants.filter(v => v.color === selectedColor);
            availableVariants.forEach(variant => { const sizeDiv = document.createElement('div'); sizeDiv.className = 'variant-swatch size-swatch'; sizeDiv.textContent = variant.size; sizeDiv.dataset.variantId = variant.id; if (variant.stock === 0) { sizeDiv.classList.add('disabled'); } sizeSelector.appendChild(sizeDiv); });
            sizeSelector.querySelectorAll('.size-swatch:not(.disabled)').forEach(swatch => { swatch.addEventListener('click', function() { selectedSize = this.textContent; sizeSelector.querySelectorAll('.size-swatch').forEach(s => s.classList.remove('selected')); this.classList.add('selected'); updateDisplay(); }); });
        }
        quantityMinusBtn.addEventListener('click', () => { let val = parseInt(quantityInput.value); if (val > 1) quantityInput.value = val - 1; });
        quantityPlusBtn.addEventListener('click', () => { let val = parseInt(quantityInput.value); if (currentVariant && val < currentVariant.stock) { quantityInput.value = val + 1; } });
        function resetDisplay() { priceDisplay.textContent = 'Fiyat için seçim yapın'; stockDisplay.textContent = 'Beden seçiniz'; addToCartBtn.disabled = true; quantityMinusBtn.disabled = true; quantityPlusBtn.disabled = true; quantityInput.value = 1; currentVariant = null; }
        function updateDisplay() {
            if (selectedColor && selectedSize) {
                currentVariant = variants.find(v => v.color === selectedColor && v.size === selectedSize);
                if (currentVariant) {
                    priceDisplay.textContent = `${currentVariant.price} TL`; quantityInput.max = currentVariant.stock;
                    if (currentVariant.stock > 0) {
                        stockDisplay.textContent = `Stok: ${currentVariant.stock} adet`; addToCartBtn.disabled = false;
                        quantityMinusBtn.disabled = false; quantityPlusBtn.disabled = false; quantityInput.value = 1;
                        const baseUrl = addToCartForm.dataset.baseAction; addToCartForm.action = baseUrl.replace('0', currentVariant.id);
                    } else { stockDisplay.textContent = 'Tükendi'; resetDisplay(); }
                }
            }
        }
    }
});