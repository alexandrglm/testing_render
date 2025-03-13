
//////// 
const themeToggle = document.getElementById('toggle-theme');

function toggleTheme() {
  const htmlElement = document.documentElement;

  if (htmlElement.getAttribute('data-theme') === 'dark') {
    htmlElement.removeAttribute('data-theme');
    localStorage.setItem('theme', 'light');

  } else {

    htmlElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  }
}


function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  const htmlElement = document.documentElement;

  if (savedTheme === 'dark') {

    htmlElement.setAttribute('data-theme', 'dark');

  } else {
   
    htmlElement.removeAttribute('data-theme');
  }
}


if (themeToggle) {

  themeToggle.addEventListener('click', toggleTheme);

}
window.addEventListener('load', loadTheme);

//////// Zoom Buttons //////// 
const zoomInButton = document.getElementById('zoom-in');
const zoomOutButton = document.getElementById('zoom-out');
const contentWrapper = document.querySelector('.content-wrapper');

let fontSize = 16;

if (zoomInButton && zoomOutButton && contentWrapper) {

  zoomInButton.addEventListener('click', () => {

    fontSize += 2;

    contentWrapper.style.fontSize = `${fontSize}px`;
    
  });

  zoomOutButton.addEventListener('click', () => {
    fontSize -= 2;
    if (fontSize < 10) fontSize = 10;
    contentWrapper.style.fontSize = `${fontSize}px`;
  });
}

//////// Export to PDF Pending //////// 
