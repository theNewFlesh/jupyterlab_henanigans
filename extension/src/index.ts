import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_henanigans extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_henanigans:plugin',
  description: 'A dark JupyterLab theme.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab_henanigans is activated!');
    const style = 'jupyterlab_henanigans/index.css';

    manager.register({
      name: 'jupyterlab_henanigans',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
