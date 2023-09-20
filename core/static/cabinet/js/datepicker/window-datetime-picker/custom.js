datetimes = document.querySelectorALl('.datetimeinput')
datetimes.forEach(e => {
    const picker = new WindowDatePicker({
      el: e,
      toggleEl: e,
});
})