"use strict";

function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
        var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor);
    }
}

function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps); return Constructor;
}

var select_product =
    function () {
        function select_product() {
            _classCallCheck(this, select_product);

            this.init();
        }

        _createClass(select_product, [{
            key: "init",
            value: function init() {
                this.fillSelectFromStates();
                this.remoteData();
            }
        }, {
            key: "getStates",
            value: function getStates() {
                return $('#select2-source-states').html();
            }
        }, {
            key: "fillSelectFromStates",
            value: function fillSelectFromStates() {
                $('#select2-single, #select2-multiple').append(this.getStates());
            }
        }, {
            key: "remoteData",
            value: function remoteData() {
                var formatRepo = function formatRepo(repo) {
                    if (repo.loading) return repo.text;
                    var markup = '';
                    markup = repo.text;
                    return markup;
                };

                var formatRepoSelection = function formatRepoSelection(repo) {
                    return repo.text;
                };

                $('#id_product_id').select2({
                    ajax: {
                        url: '/sales-products-search/',
                        dataType: 'json',
                        delay: 250,
                        data: function data(params) {
                            return {
                                q: params.term,
                                actype: params.term,
                                page: params.page
                            };
                        },
                        processResults: function processResults(data, params) {
                            params.page = params.page || 1;
                            return {
                                results: data
                            };
                        },
                        cache: true
                    },
                    escapeMarkup: function escapeMarkup(markup) {
                        return markup;
                    },
                    minimumInputLength: 1,
                    templateResult: formatRepo,
                    templateSelection: formatRepoSelection
                });
            }
        }]);

        return select_product;
    }();

$(document).on('theme:init', function () {
    new select_product();
});