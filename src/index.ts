import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @quansight-labs/jupyterlab-theme-winter extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: '@theNewFlesh/jupyterlab_henanigans',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension @theNewFlesh/jupyterlab_henanigans is activated!');
    const style = '@theNewFlesh/jupyterlab_henanigans/index.css';
    manager.register({
      name: 'JupyterLab Henanigans',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default extension;