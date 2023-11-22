function updateRectangles(svgId, labelText, averageValue, maxValue) {
  const svg = document.getElementById(svgId);
  const percentage = (averageValue * 100).toFixed(2);
  const barWidth = Math.min(averageValue, 1) * maxValue;
  const inverseWidth = maxValue - barWidth;

  svg.querySelector('.results-pip-label').textContent = `${labelText}: ${percentage}%`;
  svg.querySelector('rect:nth-child(2)').setAttribute('width', barWidth);
  svg.querySelector('rect:nth-child(3)').setAttribute('width', inverseWidth);

  //svg.querySelector('rect:nth-child(3)').setAttribute('x', (220 + barWidth) + '');
  //svg.querySelector('rect:nth-child(2)').setAttribute('x', (220 + barWidth) + '');

}