package com.addisababa.aischool.data.models

data class User(
    val id: String,
    val email: String,
    val firstName: String,
    val lastName: String,
    val role: UserRole
) {
    val fullName: String get() = "$firstName $lastName"
    val initials: String get() = "${firstName.first()}${lastName.first()}"
}

enum class UserRole {
    ADMIN,
    TEACHER,
    STUDENT,
    PARENT,
    STAFF
}