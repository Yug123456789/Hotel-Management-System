(function (window) {
  /**
   * Define the IframeEventHandler module, used to register custom
   * event handlers for `message` events on the window.
   *
   *   register(type: string, fn: function): void
   */
  var IframeEventHandler = (function () {
    var handlers = {};

    this.register = function (type, fn) {
      handlers[type] = fn;
    };

    var receiveIframeMessage = function (event) {
      var payload = parseEventData(event.data);
      var handler = handlers[payload.type];

      if (handler) {
        handler(payload);
      }
    };

    var parseEventData = function (data) {
      var parsed = data;

      // Backward-compatible parsing of `event.data` as string-serialized JSON.
      if (typeof data === 'string') {
        try {
          parsed = JSON.parse(data);
        } catch (error) {}
      }

      if (typeof parsed !== 'object') {
        return {};
      } else {
        return parsed;
      }
    };

    window.addEventListener('message', receiveIframeMessage, false);

    return this;
  })(window);

  IframeEventHandler.register('open-link', function (payload) {
    window.location = payload.href;
  });

  IframeEventHandler.register('toggle-sidebar', function (payload) {
    window.set_sidebar_toggle_state(payload.isOpen);
  });

  IframeEventHandler.register('open-upgrade-modal', function () {
    upgrade_popup();
  });

  IframeEventHandler.register('iframe-overlay-loaded', function (payload) {
    iframe_overlay_loaded(payload.name);
  });

  IframeEventHandler.register('iframe-overlay-ready', function (payload) {
    iframe_overlay_ready(payload.name);
  });

  // closing the overlay for discussion or checklist badges AND edit task/group/project overlays
  IframeEventHandler.register('close-iframe-overlay', function () {
    hide_backdrop();
    close_meta_popup();
  });

  IframeEventHandler.register('backdrop-clicked', function () {
    click_current_backdrop();
  });

  IframeEventHandler.register('token-not-refreshed', function () {
    window.location = NEW_APP_URL + 'auth';
  });
})(window);
