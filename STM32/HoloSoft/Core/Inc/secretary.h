/*
 * secretary.h
 *
 *  Created on: Jun 10, 2020
 *      Author: Guillaume
 */

#ifndef INC_SECRETARY_H_
#define INC_SECRETARY_H_



typedef enum {
	SOF = 0,
	CMD,
	STATUS,
	CNT,
	NBYTES,
	BYTE0,
	BYTE1,
	BYTE2,
	BYTE3,
	BYTE4,
	BYTE5,
	BYTE6,
	BYTE7,
	BYTE8,
	CHK,
	EndOfFrame

}SECRETARY_protocol;

typedef enum {
	ODOMETRY = 0,//!< ODOMETRY
	MOUVEMENT,   //!< MOUVEMENT
	RESTART,     //!< RESTART
	VOLTAGE      //!< VOLTAGE
}SECRETARY_cmd_ultra;

/**
 * \fn SECRETARY_dispatcher
 * \param data donnée reçu par l'uart3
 * \return void
 * \brief Reçoit les messages d'UltraBrain et appel les fonctions concerné par le message.
 */
void SECRETARY_dispatcher(uint8_t* data);
/**
 *
 * \param cmd
 * \param CNT
 */
void SECRETARY_send_to_UltraBrain(SECRETARY_cmd_ultra cmd, uint8_t CNT);
/**
 *
 */
void SECRETARY_process_main();

#endif /* INC_SECRETARY_H_ */
