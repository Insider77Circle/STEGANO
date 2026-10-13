"""Detector coverage tests — cleaner-code variant diff.

Covers every invisible-Unicode variant that cleaner-code
(goldmembrane/cleaner-code) flags but STEGANO's detector previously missed:
format-invisible chars, spacing lookalikes, and Private Use Areas.
Also guards the subdivision-flag FP whitelist against regression.
"""

import unittest

from stegano.detector import categorize, scan

# (codepoint, name) pairs extracted from cleaner-code's invisible scanner
# (src/scanner/invisible.ts) that STEGANO did not previously cover.
FORMAT_INVISIBLE_CASES = [
    (0x00AD, "soft hyphen"),
    (0x034F, "combining grapheme joiner"),
    (0x061C, "arabic letter mark"),
    (0x180E, "mongolian vowel separator"),
    (0x2060, "word joiner"),
    (0x2061, "function application"),
    (0x2062, "invisible times"),
    (0x2063, "invisible separator"),
    (0x2064, "invisible plus"),
]

SPACING_VARIANT_CASES = (
    [(0x00A0, "non-breaking space")] +
    [(cp, f"U+{cp:04X} space") for cp in range(0x2000, 0x200B)] +
    [(0x202F, "narrow no-break space"),
     (0x205F, "medium mathematical space"),
     (0x3000, "ideographic space")]
)

# (codepoint, expected-inside?) — interior + boundary points of each PUA
# range from cleaner-code's steganography scanner (src/scanner/steganography.ts).
PUA_INSIDE = [0xE000, 0xE123, 0xF8FF,          # basic PUA
              0xF0000, 0xFABCD, 0xFFFFD,       # supplementary PUA-A
              0x100000, 0x10ABCD, 0x10FFFD]    # supplementary PUA-B
PUA_OUTSIDE = [0xDFFF, 0xF900, 0xEFFFF, 0x10FFFE, 0x110000 - 1]


class TestFormatInvisible(unittest.TestCase):
    def test_each_variant_detected(self):
        for cp, name in FORMAT_INVISIBLE_CASES:
            with self.subTest(name=name, cp=hex(cp)):
                findings = scan(chr(cp))
                self.assertEqual(len(findings), 1)
                self.assertEqual(findings[0].category, "format_invisible")

    def test_categorize(self):
        for cp, name in FORMAT_INVISIBLE_CASES:
            with self.subTest(name=name):
                self.assertEqual(categorize(cp), "format_invisible")


class TestSpacingVariant(unittest.TestCase):
    def test_each_variant_detected(self):
        for cp, name in SPACING_VARIANT_CASES:
            with self.subTest(name=name, cp=hex(cp)):
                findings = scan(chr(cp))
                self.assertEqual(len(findings), 1)
                self.assertEqual(findings[0].category, "spacing_variant")

    def test_full_2000_range(self):
        text = "".join(chr(cp) for cp in range(0x2000, 0x200B))
        findings = scan(text)
        self.assertEqual(len(findings), 11)
        self.assertTrue(all(f.category == "spacing_variant" for f in findings))


class TestPrivateUse(unittest.TestCase):
    def test_inside_ranges_detected(self):
        for cp in PUA_INSIDE:
            with self.subTest(cp=hex(cp)):
                findings = scan(chr(cp))
                self.assertEqual(len(findings), 1)
                self.assertEqual(findings[0].category, "private_use")

    def test_outside_ranges_clean(self):
        for cp in PUA_OUTSIDE:
            with self.subTest(cp=hex(cp)):
                self.assertIsNone(categorize(cp))

    def test_pua_does_not_shadow_existing_categories(self):
        # U+FEFF is zero_width even though near the basic PUA; tag block
        # and VS-supplement ranges must keep their own categories.
        self.assertEqual(categorize(0xFEFF), "zero_width")
        self.assertEqual(categorize(0xE0061), "tag_block")
        self.assertEqual(categorize(0xE0101), "variation_selector_supplement")


class TestFlagWhitelistIntact(unittest.TestCase):
    FLAGS = (
        "🏴\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F",
        "🏴\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F",
        "🏴\U000E0067\U000E0062\U000E0077\U000E006C\U000E0073\U000E007F",
    )

    def test_subdivision_flags_not_flagged(self):
        for flag in self.FLAGS:
            with self.subTest(flag=flag):
                self.assertEqual(scan(flag), [])

    def test_real_tag_payload_still_detected(self):
        tag_payload = "hi\U000E0041\U000E0042"
        findings = scan(tag_payload)
        self.assertTrue(any(f.category == "tag_block" for f in findings))


class TestNoRegression(unittest.TestCase):
    def test_original_categories_unchanged(self):
        cases = [
            (0x200B, "zero_width"),
            (0x200C, "zero_width"),
            (0x200D, "zero_width"),
            (0xFEFF, "zero_width"),
            (0x200E, "bidi_control"),
            (0x202E, "bidi_control"),
            (0x2066, "bidi_control"),
            (0xFE01, "variation_selector"),
            (0xE0001, "tag_block"),
            (0xE0100, "variation_selector_supplement"),
        ]
        for cp, expected in cases:
            with self.subTest(cp=hex(cp)):
                self.assertEqual(categorize(cp), expected)

    def test_plain_text_clean(self):
        self.assertEqual(scan("The quick brown fox jumps."), [])
        self.assertEqual(scan("café naïve résumé — 100%"), [])

    def test_mixed_text_reports_all_categories(self):
        text = "a\u200bb\u00adc\u00a0d\U000E0041e\U000E0001f"
        cats = {f.category for f in scan(text)}
        self.assertEqual(cats, {"zero_width", "format_invisible",
                               "spacing_variant", "tag_block"})

    def test_private_use_in_mixed_text(self):
        text = "a" + chr(0xE123) + "b" + chr(0xFABCD) + "c"  # basic PUA + PUA-A
        cats = {f.category for f in scan(text)}
        self.assertEqual(cats, {"private_use"})


if __name__ == "__main__":
    unittest.main()
