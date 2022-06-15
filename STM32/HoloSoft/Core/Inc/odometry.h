/*
 * odometry.h
 *
 *  Created on: Jun 11, 2020
 *      Author: Guillaume
 */

#ifndef INC_ODOMETRY_H_
#define INC_ODOMETRY_H_
typedef struct{
	double speed_WheelMotor1_rpm;
	double speed_WheelMotor2_rpm;
	double speed_WheelMotor3_rpm;
	double speed_WheelMotor4_rpm;
}ODOMETRY_speed_wheel;

typedef struct{
	double speed_X;
	double speed_Y;
	double speed_teta;
	double dist_X;
	double dist_Y;
	double teta_Z;
}ODOMETRY_speed_robot;


/**
 * \fn ODOMETRY_init
 * \return Bool_e initialisation OK
 * \brief Initialise les variable utilie pour l'odometrie
 */
void ODOMETRY_init();

/**
 * \fn ODOMETRY_it_1ms
 * \return ODOMETRY_speed_wheel vitesse de chaque roue
 * \brief Fonction appelée tout les 20ms pour meusurer la vitesse de chaque roue
 */
ODOMETRY_speed_wheel ODOMETRY_it_10ms();

/**
 * \fn ODOMETRY_it_5ms
 * \return void
 * \brief fonction qui fait une moyenne de la vitesse toute les 5ms
 */
void ODOMETRY_it_5ms();
/**
 * \fn ODOMETRY_get_speed_wheels
 * \return ODOMETRY_speed_wheel
 * \brief retourne la vitesse de chaque roue
 */
ODOMETRY_speed_wheel ODOMETRY_get_speed_wheels();

/**
 * \fn ODOMETRY_get_speed_x_y
 * \param wheels_speed vitesse actuel des roues
 * \return void
 * \brief Retourne la vitesse du robot par rapport au reférentiel de la map
 */
void ODOMETRY_calcul_speed_robot(ODOMETRY_speed_wheel wheels_speed);

/**
 *
 * \return
 */
ODOMETRY_speed_robot ODOMETRY_get_speed_robot();

#endif /* INC_ODOMETRY_H_ */
