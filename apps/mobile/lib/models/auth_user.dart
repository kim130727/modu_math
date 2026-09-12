class AuthUser {
  const AuthUser({
    required this.id,
    required this.username,
    required this.email,
    this.isStaff = false,
  });

  final int id;
  final String username;
  final String email;
  final bool isStaff;

  factory AuthUser.fromJson(Map<String, dynamic> json) {
    return AuthUser(
      id: json['id'] as int? ?? 0,
      username: json['username'] as String? ?? '',
      email: json['email'] as String? ?? '',
      isStaff: json['is_staff'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'username': username,
        'email': email,
        'is_staff': isStaff,
      };
}
