/*............................Daily Bar Graphs.................................*/

const labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30];
const data = {
  labels: labels,

  datasets: [{
    label: "Daily Your Reach",
    backgroundColor: '#6363f3',
    borderRadius: 4,
    borderWidth: 1,
    data: [65, 59, 80, 81, 56, 55, 44, 65, 70, 23, 12, 32, 45, 60, 32, 23, 40, 90, 71, 62, 54, 23, 45, 65, 76, 78, 9, 5, 50, 78],
  }]
};

const config = {
  type: 'bar',
  data: data,
  options: {
    scales: {
      x: {
        title: {
          display: false,
          text: 'Month'
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: false,
          text: 'Value'
        }
      }
    }
  },
};

const ctx = document.getElementById('dailyBar').getContext('2d');
const dailyBar = new Chart(ctx, config);

/*............................Daily Bar Graphs.................................*/

/*.............................Projection Bar Graphs.............................*/

const years = ['Telugu', 'Tamil', 'Hindi', 'Kannada', 'Malayalam', 'Other'];
const values1 = [65, 70, 80, 81, 56, 75];  // First dataset
const values2 = [40, 50, 60, 75, 50, 65];  // Second dataset

const data2 = {
  labels: years,
  datasets: [
    {
      label: 'Best Case Scenario',
      backgroundColor: "#072748",
      borderRadius: 4,
      borderWidth: 1,
      data: values1,
    },
    {
      label: 'Worst Case Scenario',
      backgroundColor: '#73a8df',
      borderRadius: 4,
      borderWidth: 1,
      data: values2,
    }
  ]
};

const config2 = {
  type: 'bar',
  data: data2,
};

const ctx2 = document.getElementById('projectionBar').getContext('2d');
const projectionBar = new Chart(ctx2, config2);


/*.............................Projection Bar Graphs.............................*/


/*...........pie chart...........*/

let number = document.getElementById("pieNumber");
const pieCircleEl = document.getElementById("pieCircle");
const pieChartText = document.getElementById("pieChartText")
const pieNum = number.textContent

const pieWidth = 600 - 600 * pieNum /100;

let counter = 0;
setInterval(() =>{
    if(counter == pieNum) {
        clearInterval
    }else{
        counter += 1;
        number.textContent = counter;
        }
 }, 30);

pieChartText.textContent = pieNum
pieCircleEl.style.strokeDashoffset = pieWidth;

/*...........pie chart...........*/

/*..........Campaign Analysis.........*/
const analysisDivEl = document.getElementById("stats-analysis-div");
const analysisPercentageEl = document.getElementById("stats-analysis-percentage")
analysisDivEl.style.width = analysisPercentageEl.textContent;
/*..........Campaign Analysis.........*/
