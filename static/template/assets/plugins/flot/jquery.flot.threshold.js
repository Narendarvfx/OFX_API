/*
 * Copyright (c) 2007-2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

(function ($) {
    var options = {
        series: { threshold: null } // or { below: number, color: color spec}
    };
    
    function init(plot) {
        function thresholdData(plot, s, datapoints, below, color) {
            var ps = datapoints.pointsize, i, x, y, p, prevp,
                thresholded = $.extend({}, s); // note: shallow copy

            thresholded.datapoints = { points: [], pointsize: ps, format: datapoints.format };
            thresholded.label = null;
            thresholded.color = color;
            thresholded.threshold = null;
            thresholded.originSeries = s;
            thresholded.data = [];
 
            var origpoints = datapoints.points,
                addCrossingPoints = s.lines.show;

            var threspoints = [];
            var newpoints = [];
            var m;

            for (i = 0; i < origpoints.length; i += ps) {
                x = origpoints[i];
                y = origpoints[i + 1];

                prevp = p;
                if (y < below)
                    p = threspoints;
                else
                    p = newpoints;

                if (addCrossingPoints && prevp != p && x != null
                    && i > 0 && origpoints[i - ps] != null) {
                    var interx = x + (below - y) * (x - origpoints[i - ps]) / (y - origpoints[i - ps + 1]);
                    prevp.push(interx);
                    prevp.push(below);
                    for (m = 2; m < ps; ++m)
                        prevp.push(origpoints[i + m]);
                    
                    p.push(null); // start new segment
                    p.push(null);
                    for (m = 2; m < ps; ++m)
                        p.push(origpoints[i + m]);
                    p.push(interx);
                    p.push(below);
                    for (m = 2; m < ps; ++m)
                        p.push(origpoints[i + m]);
                }

                p.push(x);
                p.push(y);
                for (m = 2; m < ps; ++m)
                    p.push(origpoints[i + m]);
            }

            datapoints.points = newpoints;
            thresholded.datapoints.points = threspoints;
            
            if (thresholded.datapoints.points.length > 0) {
                var origIndex = $.inArray(s, plot.getData());
                // Insert newly-generated series right after original one (to prevent it from becoming top-most)
                plot.getData().splice(origIndex + 1, 0, thresholded);
            }
                
            // FIXME: there are probably some edge cases left in bars
        }
        
        function processThresholds(plot, s, datapoints) {
            if (!s.threshold)
                return;
            
            if (s.threshold instanceof Array) {
                s.threshold.sort(function(a, b) {
                    return a.below - b.below;
                });
                
                $(s.threshold).each(function(i, th) {
                    thresholdData(plot, s, datapoints, th.below, th.color);
                });
            }
            else {
                thresholdData(plot, s, datapoints, s.threshold.below, s.threshold.color);
            }
        }
        
        plot.hooks.processDatapoints.push(processThresholds);
    }
    
    $.plot.plugins.push({
        init: init,
        options: options,
        name: 'threshold',
        version: '1.2'
    });
})(jQuery);
