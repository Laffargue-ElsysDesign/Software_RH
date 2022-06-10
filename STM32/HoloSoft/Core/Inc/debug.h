/*
 * debug.h
 *
 *  Created on: 15 juin 2020
 *      Author: Guillaume
 */

#ifndef INC_DEBUG_H_
#define INC_DEBUG_H_
/**
 *
 * \param speedXr
 * \param speedYr
 * \param speedTeta
 * \param speedXw
 * \param speedYw
 * \param teta
 * \param Xr
 * \param Yr
 * \param Xw
 * \param Yw
 */
void DEBUG_update_odometry(double speedXr, double speedYr, double speedTeta, double speedXw, double speedYw, double teta, double Xr, double Yr, double Xw, double Yw);
/**
 *
 */
void DEBUG_print_odometry();
/**
 *
 * \param target_WheelMotor1_rpm
 * \param target_WheelMotor2_rpm
 * \param target_WheelMotor3_rpm
 * \param target_WheelMotor4_rpm
 * \param pid_error_WheelMotor1_rpm
 * \param pid_error_WheelMotor2_rpm
 * \param pid_error_WheelMotor3_rpm
 * \param pid_error_WheelMotor4_rpm
 * \param speed_WheelMotor1_rpm
 * \param speed_WheelMotor2_rpm
 * \param speed_WheelMotor3_rpm
 * \param speed_WheelMotor4_rpm
 */
void DEBUG_update_corrector(double target_WheelMotor1_rpm, double target_WheelMotor2_rpm, double target_WheelMotor3_rpm, double target_WheelMotor4_rpm, double pid_error_WheelMotor1_rpm, double pid_error_WheelMotor2_rpm, double pid_error_WheelMotor3_rpm, double pid_error_WheelMotor4_rpm, double speed_WheelMotor1_rpm, double speed_WheelMotor2_rpm, double speed_WheelMotor3_rpm, double speed_WheelMotor4_rpm);
/**
 *
 */
void DEBUG_print_corrector();
/**
 *
 * \param x
 * \param y
 * \param z
 */
void DEBUG_update_cmd(int16_t x, int16_t y, int16_t z);
/**
 *
 */
void DEBUG_print_cmd();
#endif /* INC_DEBUG_H_ */
