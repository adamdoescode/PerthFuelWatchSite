
// a script to show a hidden image when the user clicks on the button

// get the button element
const imageButton = document.getElementById('imageButton');
const latitudeButton = document.getElementById('latitudeButton');
const barPlotButton = document.getElementById('barPlotButton');

// get the image element
const pricesMapImg = document.getElementById('pricesMap');
const pricesByLatitude = document.getElementById('pricesByLatitude');
const brandsBarPlot = document.getElementById('brandsBarPlot');

// add a click event listener to the button
imageButton.addEventListener('click', () => {
  if (pricesMapImg.style.display === 'block') {
    // if the image is already visible, hide it
    pricesMapImg.style.display = 'none';
    return;
  } else {
      // show the image
    pricesMapImg.style.display = 'block';
  }
});
// add a click event listener to the button
latitudeButton.addEventListener('click', () => {
  if (pricesByLatitude.style.display === 'block') {
    // if the image is already visible, hide it
    pricesByLatitude.style.display = 'none';
    return;
  } else {
      // show the image
      pricesByLatitude.style.display = 'block';
  }
});
// add a click event listener to the button
barPlotButton.addEventListener('click', () => {
  if (brandsBarPlot.style.display === 'block') {
    // if the image is already visible, hide it
    brandsBarPlot.style.display = 'none';
    return;
  } else {
      // show the image
    brandsBarPlot.style.display = 'block';
  }
});
