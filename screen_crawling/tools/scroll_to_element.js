scrool_to_element = function (id_element) {
    var elementClick = $(this).attr(id_element);
    var destination = $(elementClick).offset().top;
    $('html').animate({ scrollTop: destination }, 0);
    return false;
}