import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * A plugin for the Jupyter Henanigans Theme.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@theNewFlesh/jupyterlab_henanigans:plugin',
  description: 'Henanigans theme.',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log(
      'JupyterLab plugin @theNewFlesh/jupyterlab_henanigans is activated!'
    );
    const style = '@theNewFlesh/jupyterlab_henanigans/index.css';
    manager.register({
      name: 'Henanigans',
      displayName: 'Henanigans',
      isLight: false,
      //   themeScrollbars: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
