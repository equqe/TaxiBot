function getRating(user) {
    stars = 0
    lenght = 0
    user.rides.forEach(ride =>{
        if (ride.review) {
            review = ride.review
            length += 1
            stars += review.stars
        }
    })
    return (length!=0)?(stars/length):0
}

function getDataForOptions1(work_days) {
    dates = [...new Array(30)].map((i, idx) => {
       return moment().add({days: -idx})
    }).reverse()

    data = {
        categories:[],
        work_hours:[]
    }

    work_days = work_days.filter(work_day => {if ((moment(work_day.start_date) - moment())/1000 < 2592000) return true})

    dates.forEach(date =>{
        work_hours = 0
        work_days.forEach(work_day => {
            start_date = moment(work_day.start_date)
            if (start_date.date() == date.date()) {
                base_end_date = moment(work_day.end_date)
                now = moment()
                end_date = (base_end_date < now)
                    ?base_end_date:now
                work_hours += Math.ceil(((end_date - start_date) / (1000*3600)))
            }
        })
        data.categories.push(date.format('L'))
        data.work_hours.push(work_hours)
    })

    return data
}

function getDataForColumnChart(rides) {
    dates = [...new Array(12)].map((i, index) => {
        return moment().add({month: -index})
    }).reverse()

    data = {
        data: [],
        categories: []
    }

    dates.forEach(date => {
        var a = getRidesInDate(rides, date, 'month')
        data.data.push(a.length)
        data.categories.push(date.format("MMMM"))
    })
    return data
}

function getRidesInDate(rides, date, value) {
    if (value == 'day') return rides.filter(ride => {
        start_date = moment(ride.start_date)
        return ((start_date.date() == date.date())
            &&
            (start_date.month() == date.month())
            &&
            (start_date.year() == date.year())
            )
    });
    if (value == 'month') return rides.filter(ride => {
        start_date = moment(ride.start_date)
        return ((start_date.month() == date.month())
                &&
                (start_date.year() == date.year())
            )
    }
        )
    if (value == 'week') return rides.filter(ride => {
        start_date = moment(ride.start_date)
        return ((start_date.week() == date.week())
                &&
                (start_date.year() == date.year())
            )
    });
}

function getDataForCurrentlyChartMonthly(rides, key, value) {
    now = new Date()
    // TODO: Доделать функцию для фильтрации данных

    dates = [...new Array(value)].map((i, index) => {
        return moment().add({[key]: -(index)})
    }).reverse()

    data = {
        distance: [],
        money: [],
        categories: []
    }
    dates.forEach((date, idx, array) => {
        ridesInDate = getRidesInDate(rides, date, key)

        money = 0
        distance = 0
        ridesInDate.forEach(ride => {
            money += parseInt(ride.cost);
            distance += parseInt(
                calcCrow(ride.start_location.latitude, ride.start_location.longitude, ride.end_location.latitude, ride.end_location.longitude
                ).toFixed(3))
        })

        data.money.push(money)
        data.distance.push(distance)
        data.categories.push(date.format("L"))
    })

    return data
}

function getOptions(data) {

    var options = {
            series: [{
                name: 'Прибыль',
                data: data.money
            }/*, {
                name: 'Расстояние',
                // data: [2, 22, 35, 32, 40, 25, 50, 38, 42, 28, 20, 45, 0]
                data: data.distance
            }*/],
            chart: {
                height: 240,
                type: 'area',
                toolbar: {
                    show: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            xaxis: {
                type: 'category',
                low: 0,
                offsetX: 0,
                offsetY: 0,
                show: false,
                // categories: [],
                categories: data.categories,
                labels: {
                    low: 0,
                    offsetX: 0,
                    show: false,
                },
                axisBorder: {
                    low: 0,
                    offsetX: 0,
                    show: false,
                },
            },
            markers: {
                strokeWidth: 3,
                colors: "#ffffff",
                strokeColors: [ CubaAdminConfig.primary , CubaAdminConfig.secondary ],
                hover: {
                    size: 6,
                }
            },
            yaxis: {
                low: 0,
                offsetX: 0,
                offsetY: 0,
                show: false,
                labels: {
                    low: 0,
                    offsetX: 0,
                    show: false,
                },
                axisBorder: {
                    low: 0,
                    offsetX: 0,
                    show: false,
                },
            },
            grid: {
                show: false,
                padding: {
                    left: 0,
                    right: 0,
                    bottom: -15,
                    top: -40
                }
            },
            colors: [ CubaAdminConfig.primary , CubaAdminConfig.secondary ],
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.5,
                    stops: [0, 80, 100]
                }
            },
            legend: {
                show: false,
            },
            tooltip: {
                x: {
                    format: 'MM'
                },
            },
        };
    return options
}

function updateLeftSideDataCurrentChart(data, mode) {
    leftSideItems = document.querySelector('.chart-left')
    leftSideItems.querySelector('[data-key="main"]').querySelector('#name').innerHTML = texts[mode].main

    var moneyDiv = leftSideItems.querySelector("[data-key='money']")
    var distanceDiv = leftSideItems.querySelector("[data-key='distance']")

    updateDivData(moneyDiv, data.money.reduce(reducer) + ' руб.', texts[mode].money)
    updateDivData(distanceDiv, data.distance.reduce(reducer) + ' км', texts[mode].distance)
}

function updateDivData(div, value, name) {
    div.querySelector('#value').innerHTML = value
    div.querySelector('#name').innerHTML = name
}

var reducer = (accumulator, currentValue) => accumulator + currentValue;
