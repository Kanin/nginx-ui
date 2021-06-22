import * as ConfigPage from './pages/config.mjs';
import * as SitePage from './pages/site.mjs';

let editor = null;
toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-bottom-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}


$(document).ready(function () {
    $('.ui.dropdown').dropdown();

    $('.config.item').click(function () {
        let name = $(this).html();
        load_config(name);
    });

    $('#sites').click(function () {
        load_sites()
    });

    $('#add_site').on('keyup', function (event) {
        if (event.keyCode === 13) {
            add_site()
        }
    });

    load_sites();
});

function reload_nginx() {
    $.ajax({
        type: 'POST',
        url: '/api/reload-nginx',
        statusCode: {
            200: function () {
                toastr["success"]("Nginx has been reloaded", "Success")
            },
            400: function () {
                toastr["error"]("Nginx has not been reloaded", "Error")
            }
        }
    });
}

window.reload_nginx = reload_nginx;


function load_sites() {
    $.when(fetch_html('api/sites')).then(function () {
        $('#site').hide();
        $('#site_cards').fadeIn();
    });
}


function add_site() {
    let selector = $('#add_site');
    let name = selector.val();
    if (!name) {
        return
    }
    document.activeElement.blur()
    selector.val('');

    $.ajax({
        type: 'POST',
        url: '/api/site/' + name,
        statusCode: {
            201: function () {
                toastr["success"](`${name} has been created`, "Success")
                fetch_site(name)
            },
            409: function () {
                toastr["error"](`${name} already exists!`, "Error")
            },
            500: function () {
                toastr["error"]("Cannot write to file!", "Error")
            }
        }
    });
}

window.add_site = add_site;

function enable_site(name, enable) {
    $.ajax({
        type: 'POST',
        url: '/api/site/' + name + '/enable',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            enable: enable
        }),
        statusCode: {
            200: function () {
                if (enable) {
                    toastr["success"](`${name} has been enabled`, "Success")
                } else {
                    toastr["success"](`${name} has been disabled`, "Success")
                }
                fetch_site(name);
            }
        }
    });

}

window.enable_site = enable_site;

function update_site(name) {
    let code = editor.getValue()
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'PUT',
        url: '/api/site/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: code
        }),
        statusCode: {
            200: function () {
                toastr["success"](`${name} has been updated`, "Success")
                setTimeout(function () {
                    fetch_site(name)
                }, 400)
            }
        }
    });

}

window.update_site = update_site;

function fetch_site(name) {
    fetch('api/site/' + name)
        .then(function (response) {
            response.text().then(function (text) {
                $('#editing').html(text).fadeIn();
                $('#site_cards').hide();
                editor = SitePage.render()
            });
        })
        .catch(function (error) {
            console.error(error);
        });

}

window.fetch_site = fetch_site;

function remove_site(name) {

    $.ajax({
        type: 'DELETE',
        url: '/api/site/' + name,
        statusCode: {
            200: function () {
                toastr["success"](`${name} has been removed`, "Success")
                load_sites();
            },
            400: function () {
                alert('Deleting not possible');
            }
        }
    });

}

window.remove_site = remove_site;

function fetch_html(url) {
    fetch(url)
        .then(function (response) {
            response.text().then(function (text) {
                $('#content').html(text);
            });
        })
        .catch(function (error) {
            console.error(error);
            return false;
        });
    return true;

}

function update_config(name) {
    let code = editor.getValue()
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'POST',
        url: '/api/config/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: code
        }),
        statusCode: {
            200: function () {
                toastr["success"](`${name} has been updated`, "Success")
                setTimeout(function () {
                    $('#dimmer').removeClass('active');
                }, 450);

            }
        }
    });

}

window.update_config = update_config;

function load_config(name) {
    fetch('api/config/' + name)
        .then(function (response) {
            response.text().then(function (text) {
                $('#editing').html(text).fadeIn();
                $('#site_cards').hide();
                editor = ConfigPage.render()
            });
        })
        .catch(function (error) {
            console.error(error);
        });

}