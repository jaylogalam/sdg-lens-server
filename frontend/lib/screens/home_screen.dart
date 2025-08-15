import 'package:flutter/material.dart';
import '../utils/app_colors.dart';
import '../widgets/quick_action_button.dart';
import '../widgets/category_button.dart';
import '../widgets/announcement_tile.dart';
import '../models/announcement_model.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final announcements = [
      Announcement(category: "Events", title: "School Sports Day Next Friday", date: "Dec 15", icon: ""),
      Announcement(category: "Notices", title: "New Lunch Menu Available", date: "Dec 14", icon: ""),
      Announcement(category: "Homework", title: "Math Assignment Due on Monday", date: "Dec 13", icon: ""),
      Announcement(category: "Alerts", title: "Road Closure on Main Street", date: "Dec 12", icon: ""),
      Announcement(category: "Events", title: "Parent-Teacher Conference Sign-up Open", date: "Dec 11", icon: ""),
    ];

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        centerTitle: true,
        title: const Text(
          "Announcements",
          style: TextStyle(color: AppColors.black, fontWeight: FontWeight.w600),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: CircleAvatar(
              radius: 16,
              backgroundImage: AssetImage('assets/user.png'),
            ),
          )
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        selectedItemColor: AppColors.primaryBlue,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: "Home"),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: "Search"),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: "Profile"),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Hello, John!",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            // Quick Actions
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                QuickActionButton(icon: Icons.access_time, label: "Set Reminders", onTap: () {}),
                QuickActionButton(icon: Icons.calendar_today, label: "View Calendar", onTap: () {}),
              ],
            ),
            const SizedBox(height: 24),

            // Categories
            const Text("Categories", style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              children: [
                CategoryButton(icon: Icons.event, label: "Events", onTap: () {}),
                CategoryButton(icon: Icons.notifications, label: "Notices", onTap: () {}),
                CategoryButton(icon: Icons.book, label: "Homework", onTap: () {}),
                CategoryButton(icon: Icons.warning, label: "Alerts", onTap: () {}),
              ],
            ),
            const SizedBox(height: 24),

            // Latest Announcements
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: const [
                Text("Latest Announcements", style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
                Text("View All", style: TextStyle(color: AppColors.primaryBlue)),
              ],
            ),
            const SizedBox(height: 12),

            ListView.builder(
              itemCount: announcements.length,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemBuilder: (context, index) {
                return AnnouncementTile(announcement: announcements[index]);
              },
            )
          ],
        ),
      ),
    );
  }
}
