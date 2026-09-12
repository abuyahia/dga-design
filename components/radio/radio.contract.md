# Radio Button

Native input[type=radio] inside one label, with a decorative control and label text. Group controls by name and wrap them in fieldset/legend. Checked, disabled and required use native attributes. The input is the only keyboard focus target; arrow keys and Space retain native behavior.

Visual source: official DGA Radio CSS and behavior diagram in _reference. 24px control, 15px selected dot, 48px hover area; unselected press uses gray-300; keyboard focus uses a square frame; disabled uses gray-400 and preserves the checked state. Brand and neutral appearances supported. A disabled unselected control stays empty, correcting the official web implementation selector that fills every disabled control. No JavaScript is needed.

Page Feedback composes this template and does not override its state styling. Radio inputs underlying service-rating stars remain styled by the Rating component; they are not circular choices.
