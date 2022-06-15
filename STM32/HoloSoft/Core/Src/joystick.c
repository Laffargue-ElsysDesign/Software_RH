/*
 * joystick.c
 *
 *  Created on: Jun 11, 2020
 *      Author: Guillaume
 */

#include "main.h"
#include "joystick.h"
#include "pilote.h"

#define SIZE_SPI4	14

int16_t		joystick_p_left_x, joystick_p_left_y, joystick_p_right_x, joystick_p_right_y;
uint16_t	joystick_p_lt, joystick_p_rt, joystick_vbatt;
uint16_t	joystick_buttons;
uint8_t 	spi4_rx_ok = 0;
int16_t cmd_x, cmd_y, cmd_z;

void JOYSTICK_recieve_order(uint8_t spi4_rx[]){

	spi4_rx_ok = 1;


	joystick_p_left_y	= (uint16_t)(spi4_rx[0] << 8) | spi4_rx[1];
	joystick_p_left_x	= (uint16_t)(spi4_rx[2] << 8) | spi4_rx[3];
	joystick_p_lt		= (uint16_t)(spi4_rx[4] << 8) | spi4_rx[5];
	joystick_p_right_x	= (uint16_t)(spi4_rx[6] << 8) | spi4_rx[7];
	joystick_p_right_y	= (uint16_t)(spi4_rx[8] << 8) | spi4_rx[9];
	joystick_p_rt		= (uint16_t)(spi4_rx[10] << 8) | spi4_rx[11];
	joystick_buttons	= (uint16_t)(spi4_rx[12] << 8) | spi4_rx[13];


// PK /16 ? Je sais pas mais le reste du code est basé dessus donc c'est pas très grave
	cmd_x = joystick_p_left_x / 16;
	cmd_y = joystick_p_left_y / 16;
	cmd_z = joystick_p_right_x / 16;


	// on applique un coef sur la commande pour avoir au max 13.25 rad/s par roue. On considère que cmd_x/y/z sera au max à 500 (sans unité)
	PILOTE_recieve_cmd(((double)cmd_x*883)/100000, ((double)cmd_y*883)/100000, ((double)	cmd_z*883)/100000);

	HAL_SPI_Receive_IT(&hspi4, spi4_rx, SIZE_SPI4);
}
