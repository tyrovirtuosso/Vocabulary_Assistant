// meow.js
document.addEventListener('DOMContentLoaded', function () {
    const catIcon = document.getElementById('catIcon');
    const meowText = document.getElementById('meowText');
  
    const meowOptions = [
      'Meow',
      'Purr',
      'LMeeeeow',
      'Kitty!',
      'Cat-tastic!',
      'Feline fine!',
      'Pawsitively purrfect!',
      // Add more "Meow" text options here
    ];
  
    catIcon.addEventListener('mouseenter', function () {
      const randomIndex = Math.floor(Math.random() * meowOptions.length);
      const randomMeow = meowOptions[randomIndex];
  
      meowText.textContent = randomMeow;
      meowText.classList.remove('hidden');
  
      setTimeout(function () {
        meowText.classList.add('hidden');
      }, 1000); // Adjust the delay (in milliseconds) as needed
    });
  });
  