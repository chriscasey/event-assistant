from db import Session, init_db
from models import Event, Location, Speaker
import random

init_db()

session = Session()

# Clear existing data
session.query(Event).delete()
session.query(Location).delete()
session.query(Speaker).delete()

# Realistic location names and descriptions
location_data = [
    ("Main Auditorium", "Large auditorium with 500 seats, perfect for keynotes and major presentations"),
    ("Conference Room A", "Intimate 50-seat room with modern AV equipment"),
    ("Conference Room B", "Medium-sized room accommodating 100 attendees"),
    ("Tech Hub", "Open collaborative space with workstations and networking areas"),
    ("Innovation Lab", "Hands-on workshop space with latest technology and tools"),
    ("Startup Showcase", "Exhibition area featuring emerging companies and products"),
    ("Developer Lounge", "Casual meeting space with comfortable seating and refreshments"),
    ("Workshop Studio", "Interactive learning environment with breakout areas"),
    ("Executive Boardroom", "Premium meeting space for VIP sessions and interviews"),
    ("Networking Cafe", "Casual dining area perfect for informal discussions"),
    ("Product Demo Theater", "Specialized space for live product demonstrations"),
    ("Podcast Studio", "Professional recording setup for interviews and panels"),
    ("Rooftop Terrace", "Outdoor space for networking events and breaks"),
    ("Media Center", "Press room with high-speed internet and presentation facilities"),
    ("Maker Space", "Creative workshop area with 3D printers and prototyping tools"),
    ("AI Research Lab", "Cutting-edge facility showcasing artificial intelligence innovations"),
    ("Cybersecurity Command Center", "High-tech security demonstration and training facility"),
    ("Green Energy Pavilion", "Sustainable technology showcase and discussion area"),
    ("Mobile App Corner", "Interactive space for mobile development and testing"),
    ("Cloud Computing Center", "Modern infrastructure for cloud technology demonstrations"),
    ("Data Science Hub", "Analytics and visualization workspace with large displays"),
    ("VR Experience Room", "Immersive virtual reality demonstration space"),
    ("IoT Testing Ground", "Internet of Things device showcase and interaction area"),
    ("Blockchain Booth", "Dedicated space for cryptocurrency and blockchain discussions"),
    ("Future Tech Gallery", "Exhibition space for emerging and experimental technologies")
]

# Realistic speaker names and bios
speaker_data = [
    ("Dr. Sarah Chen", "AI researcher and former Google Brain team lead, specializing in machine learning ethics"),
    ("Marcus Rodriguez", "Senior Software Engineer at Microsoft, expert in cloud architecture and DevOps"),
    ("Jennifer Kim", "Cybersecurity consultant and former NSA analyst, focusing on enterprise security"),
    ("David Thompson", "Startup founder and venture capitalist, with 3 successful exits in fintech"),
    ("Dr. Amara Okafor", "Computer science professor at Stanford, researching quantum computing applications"),
    ("Ryan O'Sullivan", "Lead mobile developer at Spotify, creator of award-winning iOS applications"),
    ("Lisa Wang", "Product manager at Netflix, expert in user experience and data-driven design"),
    ("Ahmed Hassan", "Blockchain developer and cryptocurrency advisor, early Bitcoin adopter"),
    ("Emily Johnson", "Tech journalist and podcaster, covering emerging technologies and industry trends"),
    ("Dr. James Mitchell", "Robotics engineer at Boston Dynamics, specializing in autonomous systems"),
    ("Sophia Patel", "Data scientist at Uber, expert in machine learning and predictive analytics"),
    ("Michael Brown", "Open source advocate and Linux kernel contributor, DevOps specialist"),
    ("Dr. Maria Gonzalez", "Biotech entrepreneur combining AI with medical research and drug discovery"),
    ("Kevin Lee", "Game developer and VR pioneer, founder of successful indie game studio"),
    ("Rachel Green", "Engineering manager at Tesla, expert in autonomous vehicle technology"),
    ("Dr. Robert Taylor", "Climate tech researcher focusing on sustainable computing and green energy"),
    ("Nina Petrov", "UX designer at Apple, known for innovative interface design and accessibility"),
    ("Carlos Mendoza", "Cloud security architect at Amazon Web Services, enterprise solution expert"),
    ("Dr. Helen Wu", "Neuroscientist exploring brain-computer interfaces and neural networks"),
    ("Tom Anderson", "Full-stack developer and technical writer, creator of popular programming tutorials"),
    ("Priya Sharma", "Fintech executive and former Wall Street analyst, expert in digital payments"),
    ("Dr. Paul Williams", "Quantum physicist at IBM Research, working on quantum computing hardware"),
    ("Ashley Turner", "Social media strategist and digital marketing expert, tech industry influencer"),
    ("Dr. Yuki Tanaka", "Robotics researcher at MIT, specializing in human-robot interaction"),
    ("Brandon Davis", "Mobile security expert and ethical hacker, bug bounty hunter"),
    ("Dr. Fatima Al-Rashid", "Renewable energy engineer combining IoT with smart grid technology"),
    ("Jason Clark", "DevOps engineer at GitHub, expert in continuous integration and deployment"),
    ("Dr. Isabella Romano", "Computational biologist using AI for drug discovery and genomics"),
    ("Tyler Johnson", "Gaming industry executive and esports entrepreneur"),
    ("Dr. Raj Patel", "Computer vision researcher at NVIDIA, working on autonomous driving systems"),
    ("Megan Foster", "Tech policy advisor and former government official, expert in digital governance"),
    ("Dr. Hans Mueller", "Distributed systems researcher focusing on blockchain and consensus algorithms"),
    ("Zoe Chen", "Design thinking consultant and innovation coach for Fortune 500 companies"),
    ("Dr. Samuel Kim", "Machine learning engineer at OpenAI, expert in natural language processing"),
    ("Olivia Martinez", "Startup accelerator director and angel investor in deep tech companies"),
    ("Dr. Nathan Cooper", "Augmented reality researcher at Magic Leap, computer graphics expert"),
    ("Grace Liu", "Technical product manager at Google, expert in API design and developer tools"),
    ("Dr. Erik Johansson", "Cryptocurrency researcher and digital asset portfolio manager"),
    ("Chloe Adams", "Accessibility advocate and assistive technology developer"),
    ("Dr. Alessandro Rossi", "IoT security researcher focusing on smart city infrastructure"),
    ("Maya Patel", "Growth hacker and analytics expert, helping startups scale their user base"),
    ("Dr. Connor O'Brien", "Drone technology engineer and autonomous flight systems expert"),
    ("Jade Thompson", "Sustainable tech advocate and circular economy consultant"),
    ("Dr. Lucas Zhang", "Semiconductor researcher working on next-generation computing chips"),
    ("Ava Rodriguez", "Digital transformation consultant for traditional industries"),
    ("Dr. Felix Nakamura", "Bioinformatics researcher using AI for personalized medicine"),
    ("Isla Campbell", "EdTech entrepreneur and online learning platform founder"),
    ("Dr. Omar El-Masry", "Wireless communication engineer working on 6G technology"),
    ("Ruby Singh", "Diversity and inclusion advocate in tech, former FAANG recruiter"),
    ("Dr. Gabriel Santos", "Environmental data scientist using satellite imagery and machine learning")
]

# Realistic event titles
event_titles = [
    "The Future of Artificial Intelligence in Healthcare",
    "Building Scalable Microservices Architecture",
    "Cybersecurity Best Practices for Modern Enterprises",
    "Startup Funding: From Seed to Series A",
    "Quantum Computing: Breaking the Classical Barriers",
    "Mobile App Development: iOS vs Android in 2024",
    "User Experience Design for the Next Generation",
    "Blockchain Beyond Cryptocurrency: Real-World Applications",
    "The Evolution of Tech Journalism in the Digital Age",
    "Robotics and Automation: Transforming Manufacturing",
    "Data Science Ethics: Responsible AI Implementation",
    "Open Source Software: Community-Driven Innovation",
    "Biotech Meets AI: Revolutionizing Drug Discovery",
    "Virtual Reality: From Gaming to Enterprise Solutions",
    "Autonomous Vehicles: The Road to Full Automation",
    "Climate Tech: Technology Solutions for Environmental Challenges",
    "Designing Accessible Technology for All Users",
    "Cloud Security: Protecting Data in the Digital Era",
    "Brain-Computer Interfaces: The Next Frontier",
    "Modern Web Development: Frameworks and Best Practices",
    "Fintech Revolution: The Future of Digital Payments",
    "Quantum Internet: Securing Communication with Physics",
    "Social Media Strategy for Tech Companies",
    "Human-Robot Collaboration in the Workplace",
    "Ethical Hacking: Protecting Systems Through Penetration Testing",
    "Smart Cities: IoT and Urban Infrastructure",
    "Continuous Integration and Deployment at Scale",
    "AI in Drug Discovery: Accelerating Medical Research",
    "The Business of Gaming: Industry Trends and Opportunities",
    "Computer Vision: Seeing the World Through AI",
    "Digital Policy: Governing Technology in the 21st Century",
    "Distributed Systems: Consensus and Blockchain Technology",
    "Design Thinking: Innovation Through Human-Centered Design",
    "Natural Language Processing: Understanding Human Communication",
    "Venture Capital: Investing in the Future of Technology",
    "Augmented Reality: Blending Digital and Physical Worlds",
    "API Design: Building Developer-Friendly Interfaces",
    "Cryptocurrency Market Analysis and Investment Strategies",
    "Assistive Technology: Empowering People with Disabilities",
    "IoT Security: Protecting Connected Devices",
    "Growth Hacking: Data-Driven User Acquisition",
    "Drone Technology: Applications Beyond Delivery",
    "Sustainable Technology: Building a Greener Future",
    "Next-Generation Computing: Beyond Silicon Chips",
    "Digital Transformation: Legacy Systems to Modern Architecture",
    "Bioinformatics: Decoding Life Through Data",
    "Online Learning Platforms: The Future of Education",
    "6G Wireless: The Next Generation of Connectivity",
    "Diversity in Tech: Building Inclusive Technology Teams",
    "Environmental Data Science: Climate Change Through Analytics",
    "Serverless Computing: The Future of Application Development",
    "Voice Technology: Conversational AI and Smart Assistants",
    "Wearable Technology: Health Monitoring and Fitness Tracking",
    "Tech Ethics: Moral Considerations in Software Development",
    "Edge Computing: Processing Data Where It's Generated",
    "Digital Art and NFTs: The Intersection of Technology and Creativity",
    "Autonomous Drones: Applications in Agriculture and Logistics",
    "Passwordless Authentication: The End of Traditional Security",
    "Machine Learning Operations: MLOps in Production",
    "Smart Agriculture: IoT and AI in Farming",
    "Quantum Cryptography: Unbreakable Communication",
    "No-Code Development: Democratizing Software Creation",
    "5G Networks: Enabling the Internet of Things",
    "Digital Twins: Virtual Replicas of Physical Systems",
    "Neuromorphic Computing: Brain-Inspired Computer Architecture",
    "Renewable Energy Technology: Solar, Wind, and Storage",
    "Conversational Commerce: AI-Powered Shopping Experiences",
    "Autonomous Shipping: Self-Driving Trucks and Delivery Systems",
    "Quantum Machine Learning: AI at the Quantum Scale",
    "Precision Medicine: Personalized Healthcare Through Technology",
    "Smart Manufacturing: Industry 4.0 and Automation",
    "Decentralized Finance: DeFi and the Future of Banking",
    "Extended Reality: AR, VR, and Mixed Reality Applications",
    "Autonomous Robotics: Self-Directed Machines",
    "Digital Identity: Privacy and Security in the Digital Age",
    "Sustainable Computing: Green Data Centers and Energy Efficiency",
    "Quantum Sensors: Ultra-Precise Measurement Technology",
    "Collaborative AI: Humans and Machines Working Together",
    "Smart Grid Technology: Modernizing Electrical Infrastructure",
    "Synthetic Biology: Engineering Life at the Molecular Level",
    "Autonomous Aviation: The Future of Flight",
    "Quantum Error Correction: Making Quantum Computing Reliable",
    "Digital Health: Telemedicine and Remote Patient Monitoring",
    "Intelligent Transportation: Smart Traffic and Navigation Systems",
    "Biomimetic Computing: Learning from Nature's Designs",
    "Space Technology: Satellites, Exploration, and Commercialization",
    "Autonomous Agriculture: Robotic Farming and Crop Management",
    "Quantum Advantage: When Quantum Computing Outperforms Classical",
    "Mental Health Tech: Digital Therapeutics and Wellness Apps",
    "Smart Energy: AI-Optimized Power Distribution",
    "Computational Creativity: AI-Generated Art and Music",
    "Autonomous Marine Systems: Self-Driving Ships and Submarines",
    "Quantum Networking: Building the Quantum Internet",
    "Digital Pathology: AI in Medical Diagnosis",
    "Smart Buildings: IoT and Energy Management",
    "Evolutionary Computing: Algorithms Inspired by Natural Selection",
    "Space Exploration: Mars Missions and Beyond",
    "Autonomous Retail: Cashierless Stores and Inventory Management",
    "Quantum Simulation: Modeling Complex Systems",
    "Digital Therapeutics: Software as Medicine",
    "Smart Water Management: IoT for Conservation and Quality",
    "Artificial Life: Simulating Biological Processes",
    "Lunar Technology: Infrastructure for Moon Colonization",
    "Autonomous Defense: AI in Military Applications"
]

# Create realistic locations
locations = []
for name, description in location_data:
    loc = Location(name=name, description=description)
    locations.append(loc)
session.add_all(locations)

# Create realistic speakers
speakers = []
for name, bio in speaker_data:
    sp = Speaker(name=name, bio=bio)
    speakers.append(sp)
session.add_all(speakers)

session.commit()

# Create realistic events with varied time slots
events = []
time_slots = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", 
              "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]

# Create events using realistic titles
for i, title in enumerate(event_titles):
    ev = Event(
        name=title,
        time=random.choice(time_slots),
        location_name=random.choice(locations).name,
        speaker_name=random.choice(speakers).name,
    )
    events.append(ev)

session.add_all(events)
session.commit()
session.close()
