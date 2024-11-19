_DEFAULT_INIT = """
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: forum_category
CREATE TABLE IF NOT EXISTS forum_category (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT NOT NULL, descript TEXT NOT NULL, subscribers TEXT, moderators TEXT, creator_id INTEGER NOT NULL, issued INTEGER NOT NULL);

-- Table: forum_review
CREATE TABLE IF NOT EXISTS forum_review (id INTEGER PRIMARY KEY AUTOINCREMENT, topic_id INTEGER NOT NULL, author INTEGER NOT NULL, content TEXT NOT NULL, banned INTEGER (1) NOT NULL, ban_meta TEXT NOT NULL, reaction INTEGER NOT NULL, last_edit INTEGER NOT NULL, issued INTEGER NOT NULL);

-- Table: forum_subcategory
CREATE TABLE IF NOT EXISTS forum_subcategory (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, cat_id INTEGER NOT NULL, name TEXT NOT NULL, descript TEXT, subscribers TEXT, moderators TEXT, creator_id INTEGER NOT NULL, issued INTEGER NOT NULL);

-- Table: forum_topic
CREATE TABLE IF NOT EXISTS forum_topic (id INTEGER PRIMARY KEY AUTOINCREMENT, subcat_id INTEGER NOT NULL, author INTEGER NOT NULL, name TEXT NOT NULL, preview TEXT NOT NULL, content TEXT NOT NULL, subscribers TEXT NOT NULL, banned INTEGER (1) NOT NULL, ban_meta TEXT NOT NULL, last_edit INTEGER NOT NULL, issued INTEGER NOT NULL);

-- Table: users_profile
CREATE TABLE IF NOT EXISTS users_profile (id INTEGER UNIQUE NOT NULL, name TEXT NOT NULL, avatar TEXT NOT NULL, about TEXT DEFAULT "", subs TEXT, followers TEXT);

-- Table: users_punishment
CREATE TABLE IF NOT EXISTS users_punishment (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER NOT NULL, admin_id INTEGER NOT NULL, reason TEXT NOT NULL, duration INTEGER NOT NULL, issued_at INTEGER NOT NULL);

-- Table: users_settings
CREATE TABLE IF NOT EXISTS users_settings (id INTEGER UNIQUE NOT NULL, email_new_topic_event INTEGER (1) NOT NULL DEFAULT (1), email_new_review_event INTEGER (1) NOT NULL DEFAULT (1), email_follower_event INTEGER (1) NOT NULL DEFAULT (1), email_broadcast INTEGER (1) DEFAULT (1) NOT NULL, hide_email INTEGER (1) DEFAULT (1) NOT NULL);

-- Table: users_user
CREATE TABLE IF NOT EXISTS users_user (id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT, email TEXT, password TEXT, "group" TEXT, last_seen INTEGER, registration INTEGER);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
"""

_DEFAULT_JSON_SETTINGS = {
    "terms" : "The terms were not currently set up. Please, contact administrator to set the terms of use.",
    "contacts": "Contacts were not currently set up. Please, contact administrator to set the contacts.",
    "auth_enabled": True,
    "service_mode": False,
    "mail_host": "smtp.example.com",
    "mail_port": 444,
    "mail_from": "mymail@example.com",
    "mail_user": "mymail@example.com",
    "mail_pass": "examplePassword",
    "panel_pass": "notsetup",
    "password_salt": "notsetup",
    "version": "1.0.0"
}