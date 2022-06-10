/*
 * motors.h
 *
 *  Created on: 12 juin 2020
 *      Author: Guillaume
 */

#ifndef INC_MOTORS_H_
#define INC_MOTORS_H_

#include "corrector.h"
/**
 *
 * \param pid_out
 */
void MOTORS_update(CORRECTOR_pid_out pid_out);

#endif /* INC_MOTORS_H_ */
