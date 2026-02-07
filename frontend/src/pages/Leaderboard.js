import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trophy, Medal, Award, Filter, Crown, Star, BookOpen, Info } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import leaderboardService from '../services/leaderboardService';

const PodiumItem = ({ student, rank }) => {
    let color = "bg-gray-700";
    let icon = <Award className="w-6 h-6 text-gray-400" />;
    let scale = 1;
    let yOffset = 0;
    let initialY = 50;

    if (rank === 1) {
        color = "bg-yellow-500/20 border-yellow-500/50";
        icon = <Crown className="w-8 h-8 text-yellow-400 fill-yellow-400 animate-pulse" />;
        scale = 1.1;
        yOffset = -20;
        initialY = 80;
    } else if (rank === 2) {
        color = "bg-gray-300/20 border-gray-300/50";
        icon = <Medal className="w-7 h-7 text-gray-300" />;
    } else if (rank === 3) {
        color = "bg-amber-600/20 border-amber-600/50";
        icon = <Medal className="w-6 h-6 text-amber-600" />;
    }

    return (
        <motion.div
            initial={{ y: initialY, opacity: 0 }}
            animate={{ y: yOffset, opacity: 1 }}
            transition={{ duration: 0.6, delay: rank * 0.2, type: "spring" }}
            className={`flex flex-col items-center p-4 rounded-xl border ${color} backdrop-blur-sm w-1/3 mx-2 relative`}
            style={{ transform: `scale(${scale})` }}
        >
            <div className="absolute -top-4 bg-gray-900 rounded-full p-2 border border-gray-700 shadow-xl z-20">
                {icon}
            </div>
            <div className="mt-6 flex flex-col items-center text-center w-full z-10">
                <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center text-xl font-bold text-white mb-2 shadow-lg border-2 border-gray-800">
                    {student.avatar_seed.charAt(0).toUpperCase()}
                </div>
                <h3 className="font-bold text-white text-sm md:text-lg truncate w-full px-1">{student.student_name}</h3>
                <div className="text-xl md:text-2xl font-black text-green-400 my-1">{student.metrics.score}</div>
                <div className="text-[10px] md:text-xs text-gray-400 flex flex-col gap-1 w-full bg-gray-900/40 p-2 rounded-lg mt-1">
                    <span className="flex justify-between w-full"><span>Marks</span> <span className="text-gray-200">{student.metrics.total_marks.toLocaleString()}</span></span>
                    <span className="flex justify-between w-full"><span>Acc</span> <span className="text-yellow-400">{student.metrics.accuracy}</span></span>
                </div>
            </div>
            <div className="absolute -bottom-3 px-3 py-1 bg-gray-900 rounded-full text-xs font-bold border border-gray-700 z-20">
                #{rank}
            </div>
        </motion.div>
    );
};

const ListItem = ({ student, rank }) => (
    <motion.div
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.5 + (rank * 0.1) }}
        className="flex items-center justify-between p-3 mb-2 bg-gray-800/40 hover:bg-gray-800/60 rounded-xl border border-gray-700/30 transition-all hover:border-gray-600 group"
    >
        <div className="flex items-center gap-3 md:gap-4 flex-1">
            <div className="w-8 h-8 flex items-center justify-center font-bold text-gray-500 bg-gray-900 rounded-full border border-gray-800 group-hover:text-white transition-colors">
                #{rank}
            </div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center font-bold text-sm text-gray-300 border border-gray-600">
                {student.avatar_seed.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-white truncate">{student.student_name}</h4>
                <div className="text-xs text-gray-500 flex gap-3 mt-0.5">
                    <span className="flex items-center gap-1"><Star className="w-3 h-3 text-yellow-500/80" /> {student.metrics.accuracy}</span>
                    <span className="flex items-center gap-1"><Trophy className="w-3 h-3 text-blue-500/80" /> {student.metrics.questions_attended} Solved</span>
                </div>
            </div>
        </div>
        <div className="text-right pl-2">
            <div className="text-lg font-bold text-green-400">{student.metrics.score}</div>
        </div>
    </motion.div>
);

const Leaderboard = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [leaderboardData, setLeaderboardData] = useState([]);
    const [courses, setCourses] = useState([]);
    const [filters, setFilters] = useState({
        college_id: '',
        course_id: '',
        department_id: '',
        batch_id: '',
        section_id: '',
        category: 'all',
        limit: 10
    });

    const [error, setError] = useState(null);
    const [colleges, setColleges] = useState([]);
    const [metadata, setMetadata] = useState({ departments: [], batches: [], sections: [] });
    const [isAdmin, setIsAdmin] = useState(false);
    const [isSuperAdmin, setIsSuperAdmin] = useState(false);

    // Check Admin Status & Load Initial Data
    useEffect(() => {
        const checkAdmin = async () => {
            try {
                // Try fetching colleges (SuperAdmin only)
                try {
                    const collegeList = await leaderboardService.getColleges();
                    setColleges(collegeList);
                    setIsSuperAdmin(true);
                    setIsAdmin(true); // SA is also Admin
                } catch (e) {
                    // Not SuperAdmin, check if regular Admin by trying to get metadata
                    try {
                        const meta = await leaderboardService.getMetadata();
                        setMetadata(meta);
                        setIsAdmin(true);
                    } catch (e2) {
                        setIsAdmin(false); // Student
                    }
                }
            } catch (e) {
                console.error("Auth Check Failed", e);
            }
        };
        checkAdmin();
    }, []);

    // Load Metadata when College Changes (for SuperAdmin)
    useEffect(() => {
        if (isSuperAdmin && filters.college_id) {
            leaderboardService.getMetadata(filters.college_id)
                .then(data => setMetadata(data))
                .catch(console.error);
        }
    }, [filters.college_id, isSuperAdmin]);

    // Initial load: Fetch available courses
    useEffect(() => {
        const loadCourses = async () => {
            try {
                const courseList = await leaderboardService.getCourses(filters.college_id);
                setCourses(courseList);

                // Auto-select first course if available (only for students, admins might want "All")
                // Actually, admins usually want to see course metrics too, but let's keep it optional for admins if needed
                if (!isAdmin && courseList.length > 0) {
                    setFilters(prev => ({ ...prev, course_id: courseList[0].id }));
                }
            } catch (e) {
                console.error("Failed to load courses", e);
            }
        };
        loadCourses();
    }, [filters.college_id, isAdmin]); // Re-fetch courses if college changes

    // Fetch leaderboard when filters change
    useEffect(() => {
        if (!isAdmin && courses.length > 0 && !filters.course_id) return;
        // Admins might view "All Courses" agg (if supported?), backend supports course_id=None?
        // Backend `if course_id:` logic implies optional.
        fetchData();
    }, [filters, courses, isAdmin]);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await leaderboardService.getLeaderboard(filters);
            setLeaderboardData(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (key, value) => {
        setFilters(prev => ({ ...prev, [key]: value }));
    };

    return (
        <div className="min-h-screen bg-transparent p-4 md:p-6 text-white w-full max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                <div>
                    <h1 className="text-2xl md:text-3xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500 flex items-center gap-3">
                        <Trophy className="text-yellow-400 w-8 h-8" />
                        Elite Leaderboard
                    </h1>
                    <p className="text-gray-400 mt-1 text-sm bg-gray-900/50 px-2 py-1 rounded-md inline-block">
                        {isSuperAdmin ? 'System Administrator View' : isAdmin ? 'Administrator View' : 'Top Performers within your College'}
                    </p>

                    {/* Evaluation Basis */}
                    <div className="flex items-center gap-2 mt-2 text-xs text-gray-400 bg-gray-900/60 py-1.5 px-3 rounded-lg border border-gray-800 w-fit backdrop-blur-sm">
                        <Info className="w-3 h-3 text-blue-400" />
                        <span>Score = (70% Marks) + (20% Accuracy) + (10% Activity)</span>
                    </div>
                </div>

                {/* Filters */}
                <div className="flex flex-wrap gap-2 bg-gray-900/50 p-2 rounded-xl border border-gray-800 items-center">

                    {/* SuperAdmin: College Filter */}
                    {isSuperAdmin && (
                        <div className="relative group">
                            <select
                                className="bg-gray-800 text-sm text-gray-300 pl-3 pr-8 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none appearance-none cursor-pointer hover:bg-gray-750"
                                value={filters.college_id}
                                onChange={(e) => handleFilterChange('college_id', e.target.value)}
                            >
                                <option value="" disabled>Select College</option>
                                {colleges.map(c => (
                                    <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    {/* Admin Filters: Dept, Batch, Section */}
                    {isAdmin && (
                        <>
                            <select
                                className="bg-gray-800 text-sm text-gray-300 pl-3 pr-8 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none appearance-none cursor-pointer hover:bg-gray-750"
                                value={filters.department_id}
                                onChange={(e) => handleFilterChange('department_id', e.target.value)}
                            >
                                <option value="">All Depts</option>
                                {metadata.departments.map(d => (
                                    <option key={d.id} value={d.id}>{d.name}</option>
                                ))}
                            </select>

                            <select
                                className="bg-gray-800 text-sm text-gray-300 pl-3 pr-8 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none appearance-none cursor-pointer hover:bg-gray-750"
                                value={filters.batch_id}
                                onChange={(e) => handleFilterChange('batch_id', e.target.value)}
                            >
                                <option value="">All Batches</option>
                                {metadata.batches.map(b => (
                                    <option key={b.id} value={b.id}>{b.name}</option>
                                ))}
                            </select>

                            <select
                                className="bg-gray-800 text-sm text-gray-300 pl-3 pr-8 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none appearance-none cursor-pointer hover:bg-gray-750"
                                value={filters.section_id}
                                onChange={(e) => handleFilterChange('section_id', e.target.value)}
                            >
                                <option value="">All Sections</option>
                                {metadata.sections.map(s => (
                                    <option key={s.id} value={s.id}>{s.name}</option>
                                ))}
                            </select>
                        </>
                    )}

                    {/* Assessment Type Filter */}
                    <div className="relative group">
                        <select
                            className="bg-gray-800 text-sm text-gray-300 pl-3 pr-8 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none appearance-none cursor-pointer hover:bg-gray-750"
                            value={filters.category}
                            onChange={(e) => handleFilterChange('category', e.target.value)}
                        >
                            <option value="all">All Assessments</option>
                            <option value="coding">Coding Only</option>
                            <option value="mcq">MCQ Only</option>
                        </select>
                    </div>

                    {/* Course Filter */}
                    {(courses.length > 0 || isAdmin) && (
                        <div className="relative group">
                            <Filter className="w-4 h-4 absolute left-3 top-3 text-gray-500" />
                            <select
                                className="bg-gray-800 text-sm text-gray-300 pl-9 pr-8 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none appearance-none cursor-pointer hover:bg-gray-750 min-w-[200px]"
                                value={filters.course_id}
                                onChange={(e) => handleFilterChange('course_id', e.target.value)}
                            >
                                <option value="">{isAdmin ? "All Courses" : "Select a Course"}</option>
                                {courses.map(course => (
                                    <option key={course.id} value={course.id}>{course.title}</option>
                                ))}
                            </select>
                        </div>
                    )}
                </div>
            </div>

            {/* Error State */}
            {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl mb-6 text-center text-sm">
                    {error}
                </div>
            )}

            {/* Loading State */}
            {loading ? (
                <div className="flex flex-col items-center justify-center h-64 gap-4">
                    <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-gray-500 animate-pulse text-sm">Computing Ranks...</p>
                </div>
            ) : (
                <div className="flex flex-col gap-6">
                    {leaderboardData.length === 0 ? (
                        <div className="text-center py-20 text-gray-500 bg-gray-900/30 rounded-2xl border border-gray-800 border-dashed">
                            No data available for this filter configuration.
                        </div>
                    ) : (
                        <>
                            {/* Podium Section (Top 3) */}
                            {leaderboardData.length >= 1 && (
                                <div className="flex justify-center items-end mb-4 pt-4 min-h-[250px] relative">
                                    {leaderboardData[1] && <PodiumItem student={leaderboardData[1]} rank={2} />}
                                    {leaderboardData[0] && <PodiumItem student={leaderboardData[0]} rank={1} />}
                                    {leaderboardData[2] && <PodiumItem student={leaderboardData[2]} rank={3} />}
                                </div>
                            )}

                            {/* List Section (4+) */}
                            {leaderboardData.length > 3 && (
                                <div className="bg-gray-900/40 p-3 md:p-5 rounded-3xl border border-gray-800 backdrop-blur-xl">
                                    <h3 className="text-gray-400 font-bold mb-4 px-2 uppercase text-[10px] tracking-widest">Honorable Mentions</h3>
                                    {leaderboardData.slice(3).map((student) => (
                                        <ListItem key={student.rank} student={student} rank={student.rank} />
                                    ))}
                                    <div className="text-center text-gray-600 py-4 text-xs">• End of Leaders •</div>
                                </div>
                            )}
                        </>
                    )}
                </div>
            )}

            {/* Floating 'My Rank' Card */}
            {leaderboardData.find(u => u.is_current_user) && (
                <motion.div
                    initial={{ y: 100, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                    className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-blue-600/90 to-blue-800/90 backdrop-blur-xl p-4 rounded-2xl shadow-2xl border border-blue-400/50 flex items-center gap-4 min-w-[200px]"
                >
                    <div className="flex flex-col items-center justify-center w-12 h-12 bg-white/20 rounded-full font-black text-xl shadow-inner border border-white/10">
                        #{leaderboardData.find(u => u.is_current_user).rank}
                    </div>
                    <div className="flex-1">
                        <div className="text-[10px] uppercase tracking-wider text-blue-200 font-bold">Your Rank</div>
                        <div className="font-bold text-white text-lg leading-tight">You</div>
                    </div>
                    <div className="w-px h-10 bg-blue-400/30 mx-1"></div>
                    <div className="text-right">
                        <div className="text-2xl font-black text-white tracking-tight">{leaderboardData.find(u => u.is_current_user).metrics.score}</div>
                        <div className="text-[10px] text-blue-200 uppercase tracking-wider">Score</div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default Leaderboard;
