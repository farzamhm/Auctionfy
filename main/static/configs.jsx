/**
 * The app keys and environment configuration object.
 * @attribute Configs
 * @param {String} env                 The environment.
 * @param {JSON}   Skylink             The app keys.
 * @param {String} Skylink.apiMCUKey   The MCU app key.
 * @param {String} Skylink.apiNoMCUKey The non-MCU (P2P) app key.
 * @param {Number} maxUsers            The max number of users that can connect to the app.
 * @type JSON
 * @public
 */
define([], function() {

  /*
    You need to replace these API keys and hostnames with
    your own. Then run 'grunt dev' on the console to transpile
    this file into .js
  */

  var config = {};

  switch (window.location.host) {

    case 'auctioncamp.herokuapp.com':
      config = {
        env: 'prod',
        Skylink: {
          apiMCUKey: '54b0c260-05d0-40fc-bd3e-02b30e9301e2',
          apiNoMCUKey: '54b0c260-05d0-40fc-bd3e-02b30e9301e2'
        },
      };
      break;

    case 'dev.auctioncamp.herokuapp.com':
      config = {
        env: 'dev',
        Skylink: {
          apiMCUKey: '54b0c260-05d0-40fc-bd3e-02b30e9301e2',
          apiNoMCUKey: '54b0c260-05d0-40fc-bd3e-02b30e9301e2'
        },
      };
      break;

    default:
      config = {
        env: 'local',
        Skylink: {
          apiMCUKey: '54b0c260-05d0-40fc-bd3e-02b30e9301e2',
          apiNoMCUKey: '54b0c260-05d0-40fc-bd3e-02b30e9301e2'
          
        }
      };
  }

  // Note that the UI can support up to 20 peers but it is dependant on the user's device to be able to handle.
  config.maxUsers = 4;
  return config;

});
