/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

'use strict';

var defaults = require('../core/core.defaults');
var Element = require('../core/core.element');
var helpers = require('../helpers/index');

var defaultColor = defaults.global.defaultColor;

defaults._set('global', {
	elements: {
		point: {
			radius: 3,
			pointStyle: 'circle',
			backgroundColor: defaultColor,
			borderColor: defaultColor,
			borderWidth: 1,
			// Hover
			hitRadius: 1,
			hoverRadius: 4,
			hoverBorderWidth: 1
		}
	}
});

function xRange(mouseX) {
	var vm = this._view;
	return vm ? (Math.abs(mouseX - vm.x) < vm.radius + vm.hitRadius) : false;
}

function yRange(mouseY) {
	var vm = this._view;
	return vm ? (Math.abs(mouseY - vm.y) < vm.radius + vm.hitRadius) : false;
}

module.exports = Element.extend({
	inRange: function(mouseX, mouseY) {
		var vm = this._view;
		return vm ? ((Math.pow(mouseX - vm.x, 2) + Math.pow(mouseY - vm.y, 2)) < Math.pow(vm.hitRadius + vm.radius, 2)) : false;
	},

	inLabelRange: xRange,
	inXRange: xRange,
	inYRange: yRange,

	getCenterPoint: function() {
		var vm = this._view;
		return {
			x: vm.x,
			y: vm.y
		};
	},

	getArea: function() {
		return Math.PI * Math.pow(this._view.radius, 2);
	},

	tooltipPosition: function() {
		var vm = this._view;
		return {
			x: vm.x,
			y: vm.y,
			padding: vm.radius + vm.borderWidth
		};
	},

	draw: function(chartArea) {
		var vm = this._view;
		var model = this._model;
		var ctx = this._chart.ctx;
		var pointStyle = vm.pointStyle;
		var radius = vm.radius;
		var x = vm.x;
		var y = vm.y;
		var color = helpers.color;
		var errMargin = 1.01; // 1.01 is margin for Accumulated error. (Especially Edge, IE.)
		var ratio = 0;

		if (vm.skip) {
			return;
		}

		ctx.strokeStyle = vm.borderColor || defaultColor;
		ctx.lineWidth = helpers.valueOrDefault(vm.borderWidth, defaults.global.elements.point.borderWidth);
		ctx.fillStyle = vm.backgroundColor || defaultColor;

		// Cliping for Points.
		// going out from inner charArea?
		if ((chartArea !== undefined) && ((model.x < chartArea.left) || (chartArea.right * errMargin < model.x) || (model.y < chartArea.top) || (chartArea.bottom * errMargin < model.y))) {
			// Point fade out
			if (model.x < chartArea.left) {
				ratio = (x - model.x) / (chartArea.left - model.x);
			} else if (chartArea.right * errMargin < model.x) {
				ratio = (model.x - x) / (model.x - chartArea.right);
			} else if (model.y < chartArea.top) {
				ratio = (y - model.y) / (chartArea.top - model.y);
			} else if (chartArea.bottom * errMargin < model.y) {
				ratio = (model.y - y) / (model.y - chartArea.bottom);
			}
			ratio = Math.round(ratio * 100) / 100;
			ctx.strokeStyle = color(ctx.strokeStyle).alpha(ratio).rgbString();
			ctx.fillStyle = color(ctx.fillStyle).alpha(ratio).rgbString();
		}

		helpers.canvas.drawPoint(ctx, pointStyle, radius, x, y);
	}
});
