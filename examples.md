## BASIC STRING GENERATION

16-character hex string:
  2aadb9995e299588

32-character hex string (128 bits):
  69d1ea63d90a4dfeb5ede2f897c1ac45

32-character Base64 string:
  RCDXfUBpMNl98G9dwBv308EIACM0BY0z

32-character URL-safe string:
  iK3lpr7ccCAZsCePcnB-yeXfRIfaKYZi

16-character alphanumeric string:
  7GBv8lREdc9eN0ND

12-character letters-only string:
  TaSnXzofbWbz

10-digit number string:
  7189351490

8-character custom charset string (no similar-looking chars):
  KUATG647

## BYTE GENERATION


16 random bytes (hex representation):
  3d128c06fde90cf40dba1fe1cadb369a

Security level comparison (32 bytes):
  Medium:   727f1bda29933137... (0.00ms)
  High:     a738de12842825ce... (0.00ms)
  Paranoid: c3e73dc08e876489... (0.00ms)

## NUMBER GENERATION

16-bit random number (0-65535):
  2646

32-bit random number:
  2286911117

64-bit random number:
  9616203355455297576

128-bit random number:
  124119103688530067017722098191630710387

## PASSWORD GENERATION


Default password (16 chars, 1+ digit, 1+ special):
  2kkrMBE^QafiRjOx

Strong password (20 chars, 3+ digits, 3+ special):
  MIy$IDrj4g9s!9BM!ejR

## API KEY GENERATION


API key (24 chars):
  XDVa07sq36bIfO7RGuxwnCuy

User API key with prefix:
  user_42.3beyjgX5XGNGHOjj

Service API key (paranoid security):
  svc.LUZNGPkeLyQF4xQCWjxY40aCNL2X6PbQ

## COMMON USE CASES


Session token:
  qfkKjHNmfhBg-CYjAqE3yiuggdRaMEciURn0EIDYTGWM9lEwIkipWIbY_SWO8jXl

Database record ID:
  42926e364cc6e79beb72fb3c

Email verification code:
  877218

UUID-like identifier:
  9f364a89-8c46-020d-e094-e03f28b37d7c
  
## PERFORMANCE TEST


Generating 1000 tokens (32 chars) with different security levels:

Security level: Medium
  Average: 0.005ms per token
  Range:   0.001ms - 0.097ms

Security level: High (default)
  Average: 0.008ms per token
  Range:   0.007ms - 0.089ms

Security level: Paranoid
  Average: 0.013ms per token
  Range:   0.011ms - 0.085ms

Performance summary (relative to medium):
  Medium:   1.0x (baseline)
  High:     1.8x slower
  Paranoid: 2.9x slower

Note: Actual performance may vary by system and load.
