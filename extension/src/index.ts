import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @TheNewFlesh/jupyterlab_henanigans extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@TheNewFlesh/jupyterlab_henanigans:plugin',
  description: 'A dark, easy-on-the-eyes theme for JupyterLab.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension @TheNewFlesh/jupyterlab_henanigans is activated!');
    const style = '@TheNewFlesh/jupyterlab_henanigans/index.css';

    manager.register({
      name: '@TheNewFlesh/jupyterlab_henanigans',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
