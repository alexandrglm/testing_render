/*
 FILE:        ./server/main.py STABLE
 BRANCH:        server-stable
*/
 ( () => {

    const baseCardClass = ('.card');


    document.addEventListener('DOMContentLoaded', function() {

        init3DCardEffects();
        
    });

    
    function init3DCardEffects() {
        
        const cards = document.querySelectorAll(baseCardClass);
        
        
        cards.forEach(card => {
            
            // ON HOVER (pending  add & test touchmove event)
            card.addEventListener('mousemove', (e) => {
                
                // Tilt -> Mobile OFF
                if (window.innerWidth < 768) return;
                
                const cardRect = card.getBoundingClientRect();
                
                const x = e.clientX - cardRect.left;
                const y = e.clientY - cardRect.top;
                const centerX = cardRect.width / 2;
                const centerY = cardRect.height / 2;
                const rotateX = (centerY - y) / 20;
                const rotateY = (x - centerX) / 20;
                
                
                // Apply 3D tilt to card
                card.style.transform = `translateY(-10px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                
                
                // HOVER IMG -> Parallax
                const img = card.querySelector('img');
                
                if (img) {

                    const imgOffsetX = (centerX - x) / 20;
                    const imgOffsetY = (centerY - y) / 20;
                    
                    img.style.transform = `translateY(-5px) scale(1.05) translateX(${imgOffsetX}px) translateY(${imgOffsetY}px) translateZ(30px)`;
                }
                


                // HOVER Parallax -> SUBTITLE 
                const category = card.querySelector('.category');
                if (category) {
                    category.style.transform = `translateZ(50px) translateX(${rotateY * 2}px) translateY(${rotateX * 2}px)`;
                }
            });
            

            // on NOT HOOVER
            card.addEventListener('mouseleave', () => {
                
                // Resetting

                card.style.transform = 'translateY(0) scale(1) rotateX(0) rotateY(0)';
                card.style.transition = 'all 0.5s ease';
                
                const img = card.querySelector('img');
                
                if (img) {
                    img.style.transform = 'translateY(0) scale(1) translateZ(20px)';
                    img.style.transition = 'all 0.5s ease';
                }
                

                const category = card.querySelector('.category');
                if (category) {
                    category.style.transform = 'translateZ(30px)';
                    category.style.transition = 'all 0.3s ease';
                }
                
                // %00 or less
                setTimeout(() => {
                    card.style.transition = '';
                }, 5000);
            });
        });
    }

})();
