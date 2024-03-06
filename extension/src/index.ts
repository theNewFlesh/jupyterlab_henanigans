import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the henanigans extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'henanigans:plugin',
  description: 'A dark JupyterLab theme.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension henanigans is activated!');
    const style = 'henanigans/index.css';

    manager.register({
      name: 'henanigans',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
