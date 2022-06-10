/*
 * joystick.h
 *
 *  Created on: Jun 11, 2020
 *      Author: Guillaume
 */

#ifndef INC_JOYSTICK_H_
#define INC_JOYSTICK_H_

/**
 * \fn JOYSTICK_recieve_order
 * \param spi4_rx ordre reçu par la télécommande
 * \return void
 * \brief
 */
void JOYSTICK_recieve_order(uint8_t spi4_rx[]);

#endif /* INC_JOYSTICK_H_ */
