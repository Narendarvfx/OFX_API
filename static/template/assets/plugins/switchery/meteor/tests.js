/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

'use strict';

Tinytest.add('Switchery integration', function (test) {

    var checkbox = document.createElement('input');
    checkbox.className = 'js-switch';
    var switchy = new Switchery(checkbox);

    test.instanceOf(switchy, Switchery, 'instantiation OK');
});