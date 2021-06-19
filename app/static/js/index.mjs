import * as ConfigPage from './pages/config.mjs';
import * as DomainPage from './pages/domain.mjs';

let editor = null;

$(document).ready(function () {
    $('.ui.dropdown').dropdown();

    $('.config.item').click(function () {
        let name = $(this).html();
        load_config(name);
    });

    $('#domains').click(function () {
        load_domains()
    });

    $('#add_domain').on('keyup', function (event) {
        if (event.keyCode === 13) {
            add_domain()
        }
    });

    load_domains();
});


function load_domains() {
    $.when(fetch_html('api/domains')).then(function () {
        $('#domain').hide();
        $('#domain_cards').fadeIn();
    });
}


function add_domain() {
    let selector = $('#add_domain');
    let name = selector.val();
    if (!name) {
        return
    }
    document.activeElement.blur()
    selector.val('');

    $.ajax({
        type: 'POST',
        url: '/api/domain/' + name,
        statusCode: {
            201: function () {
                fetch_domain(name)
            }
        }
    });
}
window.add_domain = add_domain;

function enable_domain(name, enable) {

    $.ajax({
        type: 'POST',
        url: '/api/domain/' + name + '/enable',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            enable: enable
        }),
        statusCode: {
            200: function () {
                fetch_domain(name);
            }
        }
    });

}
window.enable_domain = enable_domain;

function update_domain(name) {
    let code = editor.getValue()
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'PUT',
        url: '/api/domain/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: code
        }),
        statusCode: {
            200: function () {
                setTimeout(function () {
                    fetch_domain(name)
                }, 400)
            }
        }
    });

}
window.update_domain = update_domain;

function fetch_domain(name) {
    fetch('api/domain/' + name)
        .then(function (response) {
            response.text().then(function (text) {
                $('#editing').html(text).fadeIn();
                $('#domain_cards').hide();
                editor = DomainPage.render()
            });
        })
        .catch(function (error) {
            console.error(error);
        });

}
window.fetch_domain = fetch_domain;

function remove_domain(name) {

    $.ajax({
        type: 'DELETE',
        url: '/api/domain/' + name,
        statusCode: {
            200: function () {
                load_domains();
            },
            400: function () {
                alert('Deleting not possible');
            }
        }
    });

}
window.remove_domain = remove_domain;

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
                $('#domain_cards').hide();
                editor = ConfigPage.render()
            });
        })
        .catch(function (error) {
            console.error(error);
        });

}