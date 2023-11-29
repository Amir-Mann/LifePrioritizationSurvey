function updateRectangles(svgId, labelText, averageValue, maxValue, yourChoice) {
  const svg = document.getElementById(svgId);
  const percentage = (averageValue * 100).toFixed(2);
  const barWidth = averageValue * maxValue;
  const inverseWidth = maxValue - barWidth;
  console.log("Width= " + yourChoice);
  
  svg.querySelector('.results-pip-label').textContent = `${labelText}: ${percentage}%`;
  svg.querySelector('rect:nth-child(2)').setAttribute('width', barWidth);
  svg.querySelector('rect:nth-child(3)').setAttribute('width', inverseWidth);
  svg.querySelector('rect:nth-child(3)').setAttribute('x', barWidth + 120);

  if (yourChoice == 0) {
    svg.querySelector('.choice').setAttribute('x', '571.5');
  } else {
    svg.querySelector('.choice').setAttribute('x', '60');
  }
  // Adjust the x attribute for the second rectangle based on the barWidth and additional spacing
}