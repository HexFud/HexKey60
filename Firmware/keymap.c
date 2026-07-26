#include QMK_KEYBOARD_H
#include "eeprom.h"

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT(
        KC_ESC, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_MINS, KC_EQL, KC_BSPC, KC_GRV, KC_TAB, KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_RBRC, KC_BSLS, KC_PGUP, KC_CAPS, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN, KC_QUOT, KC_ENT, KC_PGDN, KC_LSFT, KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, KC_RSFT, KC_UP, KC_DEL, KC_LCTL, KC_LGUI, KC_LALT, KC_SPC, KC_RALT, MO(1), KC_RCTL, KC_LEFT, KC_DOWN, KC_RGHT
    ),
    [1] = LAYOUT(
        KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS, KC_TRNS
    ),
};

#ifdef RGBLIGHT_ENABLE
void keyboard_post_init_user(void) {
    rgblight_enable_noeeprom();
    rgblight_sethsv_noeeprom(HSV_WHITE);
    rgblight_mode_noeeprom(RGBLIGHT_MODE_STATIC_LIGHT);
}
#endif

#ifdef RAW_ENABLE

#define KEYMAP_EEPROM_MAGIC_ADDR ((void *)100)
#define KEYMAP_EEPROM_MAGIC_VALUE 0xA5

static uint16_t dynamic_layer0[MATRIX_ROWS][MATRIX_COLS];
static bool     dynamic_layer0_ready = false;

static uint16_t eeprom_addr_for(uint8_t row, uint8_t col) {
    return 101 + (row * MATRIX_COLS + col) * sizeof(uint16_t);
}

static void dynamic_layer0_save_key(uint8_t row, uint8_t col) {
    eeprom_update_word((void *)(intptr_t)eeprom_addr_for(row, col), dynamic_layer0[row][col]);
}

static void dynamic_layer0_load_or_init(void) {
    uint8_t magic = eeprom_read_byte(KEYMAP_EEPROM_MAGIC_ADDR);

    if (magic == KEYMAP_EEPROM_MAGIC_VALUE) {
        for (uint8_t r = 0; r < MATRIX_ROWS; r++) {
            for (uint8_t c = 0; c < MATRIX_COLS; c++) {
                dynamic_layer0[r][c] = eeprom_read_word((void *)(intptr_t)eeprom_addr_for(r, c));
            }
        }
    } else {
        for (uint8_t r = 0; r < MATRIX_ROWS; r++) {
            for (uint8_t c = 0; c < MATRIX_COLS; c++) {
                dynamic_layer0[r][c] = pgm_read_word(&keymaps[0][r][c]);
                dynamic_layer0_save_key(r, c);
            }
        }
        eeprom_update_byte(KEYMAP_EEPROM_MAGIC_ADDR, KEYMAP_EEPROM_MAGIC_VALUE);
    }

    dynamic_layer0_ready = true;
}

uint16_t keymap_key_to_keycode(uint8_t layer, keypos_t key) {
    if (!dynamic_layer0_ready) {
        dynamic_layer0_load_or_init();
    }
    if (layer == 0) {
        return dynamic_layer0[key.row][key.col];
    }
    return pgm_read_word(&keymaps[layer][key.row][key.col]);
}

void raw_hid_receive(uint8_t *data, uint8_t length) {
    if (length < 1) return;

    switch (data[0]) {
        case 0x01:
            if (length >= 4) {
#ifdef RGBLIGHT_ENABLE
                rgblight_setrgb(data[1], data[2], data[3]);
#endif
            }
            break;

        case 0x02:
            if (length >= 5) {
                uint8_t row = data[1];
                uint8_t col = data[2];
                uint16_t keycode = ((uint16_t)data[3] << 8) | data[4];
                if (row < MATRIX_ROWS && col < MATRIX_COLS) {
                    if (!dynamic_layer0_ready) {
                        dynamic_layer0_load_or_init();
                    }
                    dynamic_layer0[row][col] = keycode;
                    dynamic_layer0_save_key(row, col);
                }
            }
            break;
    }

    raw_hid_send(data, length);
}

#endif
