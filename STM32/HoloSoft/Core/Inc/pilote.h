/*
 * pilote.h
 *
 *  Created on: Jun 11, 2020
 *      Author: Guillaume
 */

#ifndef INC_PILOTE_H_
#define INC_PILOTE_H_

typedef struct{
	double target_WheelMotor1_rpm;
	double target_WheelMotor2_rpm;
	double target_WheelMotor3_rpm;
	double target_WheelMotor4_rpm;
}PILOTE_target_speed;
/**
 *
 * \param x en rad/s
 * \param y en rad/s
 * \param z en rad/s
 */
void PILOTE_recieve_cmd(double x, double y, double z);
void PILOTE_mouv();
void PILOTE_stop();

#endif /* INC_PILOTE_H_ */
