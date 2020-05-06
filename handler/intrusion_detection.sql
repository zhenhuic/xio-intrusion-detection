/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : intrusion_detection

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 06/05/2020 13:00:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for baobantongyong
-- ----------------------------
DROP TABLE IF EXISTS `baobantongyong`;
CREATE TABLE `baobantongyong`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of baobantongyong
-- ----------------------------

-- ----------------------------
-- Table structure for penfenshang
-- ----------------------------
DROP TABLE IF EXISTS `penfenshang`;
CREATE TABLE `penfenshang`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of penfenshang
-- ----------------------------

-- ----------------------------
-- Table structure for sawanini_1
-- ----------------------------
DROP TABLE IF EXISTS `sawanini_1`;
CREATE TABLE `sawanini_1`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sawanini_1
-- ----------------------------

-- ----------------------------
-- Table structure for sawanini_2
-- ----------------------------
DROP TABLE IF EXISTS `sawanini_2`;
CREATE TABLE `sawanini_2`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sawanini_2
-- ----------------------------

-- ----------------------------
-- Table structure for zhuanjixia
-- ----------------------------
DROP TABLE IF EXISTS `zhuanjixia`;
CREATE TABLE `zhuanjixia`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of zhuanjixia
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
