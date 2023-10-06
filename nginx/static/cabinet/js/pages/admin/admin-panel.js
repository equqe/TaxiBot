var chart1Data = getDataForChart1(clients)

var optionslinechart = {
    chart: {
        toolbar: {
            show: false
        },
        height: 170,
        type: 'area'
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    xaxis: {
        show: false,
        type: 'date',
        categories: chart1Data.categories,
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    grid: {
        show: false,
        padding: {
            left: 0,
            right: 0,
            bottom: -40
        }
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'light',
            type: 'vertical',
            shadeIntensity: 0.4,
            inverseColors: false,
            opacityFrom: 0.8,
            opacityTo: 0.2,
            stops: [0, 100]
        },

    },
    colors:[CubaAdminConfig.primary],

    series: [
        {
        	name: "Кол-во новых клиентов",
            data: chart1Data.data
        }
    ],
    tooltip: {
        x: {
            format: 'dd.MM.yy'
        }
    }
};

var chartlinechart = new ApexCharts(
    document.querySelector("#chart-widget1"),
    optionslinechart
);

chartlinechart.render();


var chart2Data = getDataForChart1(drivers)
/*Line chart2*/
var optionslinechart2 = {
    chart: {
        toolbar: {
            show: false
        },
        height: 170,
        type: 'area'
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    xaxis: {
        show: false,
        type: 'date',
        categories: chart2Data.categories,
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    grid: {
        show: false,
        padding: {
            left: 0,
            right: 0,
            bottom: -40
        }
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'light',
            type: 'vertical',
            shadeIntensity: 0.4,
            inverseColors: false,
            opacityFrom: 0.8,
            opacityTo: 0.2,
            stops: [0, 100]
        }

    },
    colors:[CubaAdminConfig.secondary],
    series: [
        {
            name: 'Кол-во новых водителей',
            data: chart2Data.data
        }
    ],
    tooltip: {
        x: {
            format: 'dd.MM.yy'
        }
    }
};

var chartlinechart2 = new ApexCharts(
    document.querySelector("#chart-widget2"),
    optionslinechart2
);
chartlinechart2.render();

var chart3Data = getDataForChart3(orders)
/*Line chart3*/
var optionslinechart3 = {
    chart: {
        toolbar: {
            show: false
        },
        height: 170,
        type: 'area'
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    xaxis: {
        show: false,
        type: 'date',
        categories: chart3Data.categories,
        labels: {
            show: false,
        },
        axisBorder: {
            show: false,
        },
    },
    grid: {
        show: false,
        padding: {
            left: 0,
            right: 0,
            bottom: -40
        }
    },
    fill: {
        colors:['#7366ff'],
        type: 'gradient',
        gradient: {
            shade: 'light',
            type: 'vertical',
            shadeIntensity: 0.4,
            inverseColors: false,
            opacityFrom: 0.8,
            opacityTo: 0.2,
            stops: [0, 100]
        },

    },
    colors:['#7366ff'],

    series: [
        {
        	name: "Кол-во поездок",
            data: chart3Data.data
        }
    ],
    tooltip: {
        x: {
            format: 'dd.MM.yy'
        }
    }
};

var chartlinechart3 = new ApexCharts(
    document.querySelector("#chart-widget3"),
    optionslinechart3
);
chartlinechart3.render();


var weeklyData = getDataForCurrentlyChartMonthly(orders, 'day', 7)
var monthlyData = getDataForCurrentlyChartMonthly(orders, 'day', 30)
var yearlyData = getDataForCurrentlyChartMonthly(orders, 'month', 12)

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


