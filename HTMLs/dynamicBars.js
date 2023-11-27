function updateRectangles(svgId, labelText, averageValue, maxValue) {
  console.log("hej");

  const svg = document.getElementById(svgId);
  const percentage = (averageValue * 100).toFixed(2);
  const barWidth = averageValue * maxValue;
  const inverseWidth = maxValue - barWidth;
  console.log("Width= " + barWidth);
  
  svg.querySelector('.results-pip-label').textContent = `${labelText}: ${percentage}%`;
  svg.querySelector('rect:nth-child(2)').setAttribute('width', barWidth);
  svg.querySelector('rect:nth-child(3)').setAttribute('width', inverseWidth);
  svg.querySelector('rect:nth-child(3)').setAttribute('x', barWidth + 120);
  // Adjust the x attribute for the second rectangle based on the barWidth and additional spacing
}