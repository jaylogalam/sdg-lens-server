import 'package:flutter/material.dart';
import '../utils/app_colors.dart';
import '../models/announcement_model.dart';

class AnnouncementTile extends StatelessWidget {
  final Announcement announcement;

  const AnnouncementTile({super.key, required this.announcement});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(vertical: 6),
      leading: CircleAvatar(
        backgroundColor: AppColors.lightGray,
        child: Icon(Icons.calendar_today, color: AppColors.primaryBlue, size: 18),
      ),
      title: Text(
        announcement.title,
        style: const TextStyle(fontWeight: FontWeight.w500),
      ),
      subtitle: Text(
        announcement.category,
        style: const TextStyle(color: AppColors.grayText, fontSize: 13),
      ),
      trailing: Text(
        announcement.date,
        style: const TextStyle(color: AppColors.grayText, fontSize: 13),
      ),
    );
  }
}
