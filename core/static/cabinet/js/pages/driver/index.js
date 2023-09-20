user_rating = getRating(user)
var options4 = {
  series: [((user_rating/5)*100).toFixed(0)],
  chart: {
    height: 240,
    type: 'radialBar',
    offsetY: -10,
      toolbar: {
        show: false,
          tools: {
            download: true
          }
      }
  },
    legend:{
      show: false
    },
  plotOptions: {
    radialBar: {
      startAngle: -135,
      endAngle: 135,
      inverseOrder: true,
      hollow: {
        margin: 5,
        size: '60%',
        imageWidth: 140,
        imageHeight: 140,
        imageClipped: false,
      },
      track: {
        opacity: 0.4,
        colors: CubaAdminConfig.primary
      },
      dataLabels: {
        enabled: false,
        enabledOnSeries: undefined,
        textAnchor: 'middle',
        distributed: false,
        offsetX: 0,
        offsetY: 0,

        style: {
          fontSize: '14px',
          fontFamily: 'Helvetica, Arial, sans-serif',
          fill:['#2b2b2b'],

        },
      },
    }
  },

  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      shadeIntensity: 0.15,
      inverseColors: false,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [0, 100],
      gradientToColors: ['#a927f9'],
      type: 'horizontal'
    },
  },
  stroke: {
    dashArray: 15,
    strokecolor: ['#ffffff']
  },

  labels: [user_rating.toFixed(2)],

  colors: [ CubaAdminConfig.primary ],

};
var chart4 = new ApexCharts(document.querySelector("#riskfactorchart"),
  options4
);

chart4.render();


// WorkDays


options1Data = getDataForOptions1(user.driver.work_days)
var options1 = {
  series: [{
    name: 'Рабочие часы',
    data: options1Data.work_hours
  }],
  chart: {
    height: 150,
    type: 'area',
    toolbar: {
      show: false
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    width: 0
  },
  xaxis: {
    type: 'date',
    categories: options1Data.categories

  },
  tooltip: {
    x: {
      format: 'dd/MM/yy HH:mm'
    },
  },
  legend: {
    show: false,
  },
  grid: {
    show: false,
    padding: {
      left: 0,
      right: 0,
      top: 0,
      bottom: -40,
    }
  },
  fill: {
    type: 'gradient',
    opacity: [1, 0.4, 0.25],
    gradient: {
      shade: 'light',
      type: 'horizontal',
      shadeIntensity: 1,
      gradientToColors: ['#a26cf8', '#a927f9', '#7366ff'],
      opacityFrom: [1, 0.4, 0.25],
      opacityTo: [1, 0.4, 0.25],
      stops: [30, 100],
      colorStops: []
    },
    colors: [ CubaAdminConfig.primary , CubaAdminConfig.primary , CubaAdminConfig.primary],
  },
  colors: [CubaAdminConfig.primary, CubaAdminConfig.secondary, CubaAdminConfig.secondary],
};

var chart1 = new ApexCharts(document.querySelector("#spaline-chart"),
  options1
);

chart1.render();
document.querySelector('#chart-options1').innerHTML = options1Data.work_hours.reduce((x,y) => x+y)




// total earning
var options2 = {
  series: [{
    name: 'Daily',
    data: [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50,
      1.55, 1.50, 1.45, 1.40, 1.35, 1.30, 1.25, 1.20, 1.15, 1.10, 1.05, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35
    ]
  },
  {
    name: 'Weekly',
    data: [-0.40, -0.50, -0.60, -0.70, -0.80, -0.90, -1.10, -1.15, -1.20, -1.25, -1.30, -1.35, -1.40, -1.45, -1.50,
    -1.55, -1.50, -1.45, -1.40, -1.35, -1.30, -1.25, -1.20, -1.15, -1.10, -1.05, -0.90, -0.85, -0.80, -0.75, -0.70, -0.65, -0.60, -0.55, -0.50, -0.45, -0.40, -0.35
    ]
  },
  {
    name: 'Monthly',
    data: [-1.35, -1.45, -1.55, -1.65, -1.75, -1.85, -1.95, -2.15, -2.25, -2.35, -2.45, -2.55, -2.65, -2.75, -2.85,
    -2.95, -3.00, -3.10, -3.20, -3.25, -3.10, -3.00, -2.95, -2.85, -2.75, -2.65, -2.55, -2.45, -2.35, -2.25, -2.15, -1.95, -1.85, -1.75, -1.65, -1.55, -1.45, -1.35
    ]
  },
  {
    name: 'Yearly',
    data: [1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95, 2.15, 2.25, 2.35, 2.45, 2.55, 2.65, 2.75, 2.85,
    2.95, 3.00, 3.10, 3.20, 3.25, 3.10, 3.00, 2.95, 2.85, 2.75, 2.65, 2.55, 2.45, 2.35, 2.25, 2.15, 1.95, 1.85, 1.75, 1.65, 1.55, 1.45, 1.35
    ]
  }
  ],
  chart: {
    type: 'bar',
    height: 320,
    stacked: true,
    toolbar: {
      show: false
    },
  },
 colors: [ CubaAdminConfig.primary , CubaAdminConfig.primary , CubaAdminConfig.primary , CubaAdminConfig.primary ],
  plotOptions: {
    bar: {
      vertical: true,
      columnWidth: '40%',
      barHeight: '80%',
      startingShape: 'rounded',
      endingShape: 'rounded'
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    width: 0

  },
  legend: {
    show: false,
  },
  grid: {
    xaxis: {
      lines: {
        show: false
      }
    },
    yaxis: {
      lines: {
        show: false
      }
    },
  },
  yaxis: {
    min: -5,
    max: 5,
    show: false,
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },

  },
  tooltip: {
    shared: true,
    x: {
      formatter: function (val) {
        return val
      }
    },
    y: {
      formatter: function (val) {
        return Math.abs(val) + "%"
      }
    }
  },
  xaxis: {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug',
      'Sep', 'Oct', 'Nov', 'Dec'
    ],
    labels: {
      show: true
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    }

  },

  fill: {
    // type: 'solid',
    opacity: [0.8, 0.8, 0.2, 0.2],
    colors: [function({ value, seriesIndex, w }) {
      if(value < 0.75) {
          return "#a26cf8"
      } else {
          return CubaAdminConfig.primary
      }
    }]
  }
};

var chart2 = new ApexCharts(document.querySelector("#negative-chart"),
  options2
);

chart2.render();




chart3Data = getDataForColumnChart(user.rides)
// month total
var options3 = {
  series: [{
    name: 'Количество поездок',
    data: chart3Data.data
  }],
  chart: {
    height: 105,
    type: 'bar',
    stacked: true,
    toolbar: {
      show: false
    },
  },
  plotOptions: {
    bar: {
      dataLabels: {
        position: 'top', // top, center, bottom
      },

      columnWidth: '20%',
      startingShape: 'rounded',
      endingShape: 'rounded'
    }
  },
  dataLabels: {
    enabled: false,
    offsetY: -10,
    style: {
      fontSize: '12px',
      colors: [ CubaAdminConfig.primary ]
    }
  },

  xaxis: {
    categories: chart3Data.categories,
    position: 'bottom',

    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    crosshairs: {
      fill: {
        type: 'gradient',
        gradient: {
          colorFrom: '#7366ff',
          colorTo: '#c481ec',
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        }
      }
    },
    tooltip: {
      enabled: true,
    },
    labels: {
      show: false
    }

  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false,
    }

  },
  grid: {
    show: false,
    padding: {
      top: -35,
      right: -10,
      bottom: -20,
      left: -10
    },
  },
  colors: [ CubaAdminConfig.primary ],

};


var chart3 = new ApexCharts(document.querySelector("#column-chart"),
  options3
);


chart3.render();

//This function takes in latitude and longitude of two location and returns the distance between them as the crow flies (in km)


weeklyData = getDataForCurrentlyChartMonthly(user.rides, key='day', value=7)
monthlyData = getDataForCurrentlyChartMonthly(user.rides, key='day', value=30)
yearlyData = getDataForCurrentlyChartMonthly(user.rides, key='month', value=12)



var options = {
        week: getOptions(weeklyData),
        month: getOptions(monthlyData),
        year: getOptions(yearlyData)
}

var texts = {
        week: {
            main: 'Последняя неделя',
            money: "Заработано за последнюю неделю",
            distance: "Дистанция за последнюю неделю",
            rides: "Поездок в последнюю неделю"
        },
        month: {
            main: 'Последний месяц',
            money: "Заработано за последний месяц",
            distance: "Дистанция за последний месяц",
            rides: "Поездок в последний месяц"
        },
        year: {
            main: 'Последний год',
            money: "Заработано за год",
            distance: "Дистанция за год",
            rides: "Поездок за год"
        },
}



var currentChartButtons = document.querySelectorAll('#current-chart--pick-mode')
currentChartButtons.forEach((e, idx, array) =>{
    // Добавляем листенер при нажатии
    e.addEventListener('click', function(event) {
        // Запрашиваем режим
        var mode = event.target.dataset['mode']
        // Делаем все элемент неактивными
        array.forEach(e => e.classList.remove('active'))
        // Делаем кликнутый элемент активным
        e.classList.add('active')
        // Обновляем график
        chartMonthly.updateOptions(options[mode]);
        if (mode=='week') updateLeftSideDataCurrentChart(weeklyData, 'week')
        if (mode=='month') updateLeftSideDataCurrentChart(monthlyData, 'month')
        if (mode=='year') updateLeftSideDataCurrentChart(yearlyData, 'year')
    })
})


updateLeftSideDataCurrentChart(monthlyData, 'month')
var chartMonthly = new ApexCharts(document.querySelector("#chart-currently"), options['month']);
chartMonthly.render();

// Initialize leaflet map
const user_location = [user.location.latitude, user.location.longitude]
var map = L.map('map').setView(user_location, 13);
// Connect png map from open street map
L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data <a target="_blank" href="http://www.openstreetmap.org">OpenStreetMap.org</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
  maxZoom: 17,
  minZoom: 9
}).addTo(map);

var marker = L.marker(user_location).addTo(map);







