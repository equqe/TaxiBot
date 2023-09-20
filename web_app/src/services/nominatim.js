export const nominatimProcessResult = result => {
    if (result.address && result.address.road) {
        if (result.address.city || result.address.town || result.address.village) {
            result.display_name = result.address.city || result.address.town || result.address.village

            if (result.address.road) {
                result.display_name += ", " + result.address.road
            }

            if (result.address.house_number) {
                result.display_name += ", " + result.address.house_number
            }
        }
    }


    result.set_name = result.display_name
    if (result.address) {
        if (result.address.road) {
            result.set_name = result.address.road
            if (result.address.house_number) {
                result.set_name = result.set_name + ", " + result.address.house_number
            }
        } else if (result.address.city) {
            result.set_name = result.address.city
        } else if (result.address.town) {
            result.set_name = result.address.town
        } else if (result.address.natural) {
            result.set_name = result.address.natural
        } else if (result.address.hamlet) {
            result.set_name = result.address.hamlet
        } else if (result.address.village) {
            result.set_name = result.address.village
        } else if (result.address.state) {
            result.set_name = result.address.state
        }
    }
    return result
}