// clients
DATES = [...new Array(7)].map((i, index) => {
        return moment().add({day: -index})
    }).reverse()


function getUsersWhichRegisterInDay(users, date) {
    // Возвращает список пользователей, которые зарегистрировались в данный день 

    list = []

    users.forEach(user => {
        regDate = moment(user.date_joined)
        if (
            (regDate.day() == date.day())
            &&
            (regDate.month() == date.month())
            &&
            (regDate.year() == date.year())
            ) {
            list.push(user)
        }
    })

    return list
}

function getDataForChart1(users) {
    data = {
        data: [],
        categories: []
    }

    DATES.forEach(date => {
        var a = getUsersWhichRegisterInDay(users, date) // func from drivers/utils.js
        data.data.push(a.length)
        data.categories.push(date.format("L"))
    })

    return data
}

function getDataForChart3(rides) {
    data = {
        data: [],
        categories: []
    }

    DATES.forEach(date => {
        var a = getRidesInDate(rides, date, 'day') // func from drivers/utils.js
        data.data.push(a.length)
        data.categories.push(date.format("L"))
    })
    return data
}  


