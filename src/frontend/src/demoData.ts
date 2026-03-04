/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/** Demo seed data — precomputed knowledge graph for offline demo. */

import type { GraphNode, GraphEdge } from './types';

const GRAPH_ID = 'demo-graph-001';

export const DEMO_NODES: GraphNode[] = [
  { id: 'n01', graphId: GRAPH_ID, label: 'Physics', category: 'physics', description: 'The fundamental science of matter, energy, and their interactions. Physics seeks to understand the natural world through observation and mathematical frameworks.', positionX: 400, positionY: 300, cid: 'a1b2c3d4', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n02', graphId: GRAPH_ID, label: 'Quantum Mechanics', category: 'physics', description: 'The branch of physics dealing with phenomena at nanoscopic scales, where the action is on the order of the Planck constant.', positionX: 550, positionY: 200, cid: 'b2c3d4e5', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n03', graphId: GRAPH_ID, label: 'Thermodynamics', category: 'physics', description: 'The branch of physics dealing with heat, work, temperature, and their relation to energy and entropy.', positionX: 300, positionY: 450, cid: 'c3d4e5f6', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n04', graphId: GRAPH_ID, label: 'Electromagnetism', category: 'physics', description: 'The study of electromagnetic force, one of the four fundamental forces, encompassing electric and magnetic fields.', positionX: 550, positionY: 400, cid: 'd4e5f6g7', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n05', graphId: GRAPH_ID, label: 'Mathematics', category: 'mathematics', description: 'The abstract science of number, quantity, and space, studied either as abstract concepts or as applied to other disciplines.', positionX: 200, positionY: 250, cid: 'e5f6g7h8', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n06', graphId: GRAPH_ID, label: 'Calculus', category: 'mathematics', description: 'The mathematical study of continuous change, involving derivatives and integrals.', positionX: 100, positionY: 350, cid: 'f6g7h8i9', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n07', graphId: GRAPH_ID, label: 'Linear Algebra', category: 'mathematics', description: 'The branch of mathematics concerning linear equations, linear maps, and their representations in vector spaces and through matrices.', positionX: 100, positionY: 180, cid: 'g7h8i9j0', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n08', graphId: GRAPH_ID, label: 'Chemistry', category: 'chemistry', description: 'The scientific study of the properties, composition, and transformations of matter.', positionX: 650, positionY: 300, cid: 'h8i9j0k1', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n09', graphId: GRAPH_ID, label: 'Organic Chemistry', category: 'chemistry', description: 'The study of the structure, properties, composition, reactions, and synthesis of carbon-containing compounds.', positionX: 750, positionY: 200, cid: 'i9j0k1l2', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n10', graphId: GRAPH_ID, label: 'Biochemistry', category: 'chemistry', description: 'The study of chemical processes within and relating to living organisms.', positionX: 800, positionY: 350, cid: 'j0k1l2m3', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n11', graphId: GRAPH_ID, label: 'Biology', category: 'biology', description: 'The natural science that studies life and living organisms, including their structure, function, growth, evolution, and distribution.', positionX: 700, positionY: 500, cid: 'k1l2m3n4', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n12', graphId: GRAPH_ID, label: 'Genetics', category: 'biology', description: 'The study of genes, genetic variation, and heredity in organisms.', positionX: 850, positionY: 450, cid: 'l2m3n4o5', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n13', graphId: GRAPH_ID, label: 'Ecology', category: 'biology', description: 'The study of relationships between living organisms and their environment.', positionX: 600, positionY: 550, cid: 'm3n4o5p6', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n14', graphId: GRAPH_ID, label: 'Computer Science', category: 'computer_science', description: 'The study of computation, automation, and information, encompassing both theoretical and practical disciplines.', positionX: 150, positionY: 500, cid: 'n4o5p6q7', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n15', graphId: GRAPH_ID, label: 'Algorithms', category: 'computer_science', description: 'A finite sequence of well-defined instructions for solving a class of problems or performing a computation.', positionX: 50, positionY: 500, cid: 'o5p6q7r8', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n16', graphId: GRAPH_ID, label: 'Machine Learning', category: 'computer_science', description: 'A subset of AI that enables systems to learn and improve from experience without being explicitly programmed.', positionX: 250, positionY: 600, cid: 'p6q7r8s9', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n17', graphId: GRAPH_ID, label: 'Cryptography', category: 'computer_science', description: 'The practice and study of techniques for secure communication in the presence of adversaries.', positionX: 50, positionY: 400, cid: 'q7r8s9t0', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n18', graphId: GRAPH_ID, label: 'Optics', category: 'physics', description: 'The branch of physics that studies the behavior and properties of light and its interactions with matter.', positionX: 650, positionY: 150, cid: 'r8s9t0u1', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n19', graphId: GRAPH_ID, label: 'Astronomy', category: 'astronomy', description: 'The scientific study of celestial objects, space, and the physical universe as a whole.', positionX: 450, positionY: 100, cid: 's9t0u1v2', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n20', graphId: GRAPH_ID, label: 'Cosmology', category: 'astronomy', description: 'The study of the origin, evolution, and eventual fate of the universe.', positionX: 500, positionY: 50, cid: 't0u1v2w3', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n21', graphId: GRAPH_ID, label: 'Statistics', category: 'mathematics', description: 'The discipline that concerns the collection, organization, analysis, interpretation, and presentation of data.', positionX: 200, positionY: 100, cid: 'u1v2w3x4', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n22', graphId: GRAPH_ID, label: 'Probability', category: 'mathematics', description: 'The branch of mathematics concerned with probability, the analysis of random phenomena.', positionX: 300, positionY: 100, cid: 'v2w3x4y5', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n23', graphId: GRAPH_ID, label: 'Earth Science', category: 'earth_science', description: 'The study of the Earth and its neighbors in space, including geology, meteorology, and oceanography.', positionX: 500, positionY: 500, cid: 'w3x4y5z6', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n24', graphId: GRAPH_ID, label: 'Geology', category: 'earth_science', description: 'The study of the solid Earth, the rocks of which it is composed, and the processes by which they change over time.', positionX: 450, positionY: 600, cid: 'x4y5z6a7', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n25', graphId: GRAPH_ID, label: 'Particle Physics', category: 'physics', description: 'The study of the fundamental constituents of matter and the forces between them.', positionX: 500, positionY: 150, cid: 'y5z6a7b8', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n26', graphId: GRAPH_ID, label: 'Neuroscience', category: 'biology', description: 'The scientific study of the nervous system, including the brain, spinal cord, and peripheral nerves.', positionX: 800, positionY: 550, cid: 'z6a7b8c9', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n27', graphId: GRAPH_ID, label: 'Topology', category: 'mathematics', description: 'The study of geometric properties that are preserved under continuous deformations of objects.', positionX: 50, positionY: 250, cid: 'a7b8c9d0', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n28', graphId: GRAPH_ID, label: 'Relativity', category: 'physics', description: 'Einstein\'s theories of special and general relativity, describing gravity as geometry of spacetime.', positionX: 350, positionY: 200, cid: 'b8c9d0e1', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n29', graphId: GRAPH_ID, label: 'Information Theory', category: 'computer_science', description: 'The mathematical study of the quantification, storage, and communication of information.', positionX: 150, positionY: 600, cid: 'c9d0e1f2', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n30', graphId: GRAPH_ID, label: 'Molecular Biology', category: 'biology', description: 'The study of biology at the molecular level, focusing on DNA, RNA, and protein biosynthesis.', positionX: 900, positionY: 400, cid: 'd0e1f2g3', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n31', graphId: GRAPH_ID, label: 'Wave Theory', category: 'physics', description: 'The study of wave phenomena including sound waves, light waves, and quantum wave functions.', positionX: 600, positionY: 250, cid: 'e1f2g3h4', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n32', graphId: GRAPH_ID, label: 'Number Theory', category: 'mathematics', description: 'The study of integers and integer-valued functions, including primes and divisibility.', positionX: 50, positionY: 150, cid: 'f2g3h4i5', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n33', graphId: GRAPH_ID, label: 'Climate Science', category: 'earth_science', description: 'The study of Earth\'s climate system, including atmospheric, oceanic, and surface processes.', positionX: 550, positionY: 600, cid: 'g3h4i5j6', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n34', graphId: GRAPH_ID, label: 'Evolution', category: 'biology', description: 'The change in heritable characteristics of biological populations over successive generations.', positionX: 750, positionY: 500, cid: 'h4i5j6k7', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
  { id: 'n35', graphId: GRAPH_ID, label: 'Graph Theory', category: 'mathematics', description: 'The study of graphs as mathematical structures used to model pairwise relations between objects.', positionX: 200, positionY: 450, cid: 'i5j6k7l8', metadata: null, createdAt: '2026-01-01T00:00:00Z', updatedAt: '2026-01-01T00:00:00Z' },
];

export const DEMO_EDGES: GraphEdge[] = [
  { id: 'e01', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n02', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e02', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n03', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e03', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n04', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e04', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n18', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e05', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n25', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e06', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n28', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e07', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n31', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e08', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n06', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e09', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n07', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e10', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n21', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e11', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n22', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e12', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n27', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e13', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n32', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e14', graphId: GRAPH_ID, sourceId: 'n05', targetId: 'n35', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e15', graphId: GRAPH_ID, sourceId: 'n08', targetId: 'n09', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e16', graphId: GRAPH_ID, sourceId: 'n08', targetId: 'n10', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e17', graphId: GRAPH_ID, sourceId: 'n11', targetId: 'n12', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e18', graphId: GRAPH_ID, sourceId: 'n11', targetId: 'n13', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e19', graphId: GRAPH_ID, sourceId: 'n11', targetId: 'n26', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e20', graphId: GRAPH_ID, sourceId: 'n11', targetId: 'n30', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e21', graphId: GRAPH_ID, sourceId: 'n11', targetId: 'n34', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e22', graphId: GRAPH_ID, sourceId: 'n14', targetId: 'n15', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e23', graphId: GRAPH_ID, sourceId: 'n14', targetId: 'n16', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e24', graphId: GRAPH_ID, sourceId: 'n14', targetId: 'n17', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e25', graphId: GRAPH_ID, sourceId: 'n14', targetId: 'n29', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e26', graphId: GRAPH_ID, sourceId: 'n01', targetId: 'n05', label: 'depends_on', weight: 2.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e27', graphId: GRAPH_ID, sourceId: 'n02', targetId: 'n07', label: 'requires', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e28', graphId: GRAPH_ID, sourceId: 'n08', targetId: 'n01', label: 'related_to', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e29', graphId: GRAPH_ID, sourceId: 'n10', targetId: 'n11', label: 'bridges', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e30', graphId: GRAPH_ID, sourceId: 'n16', targetId: 'n21', label: 'uses', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e31', graphId: GRAPH_ID, sourceId: 'n16', targetId: 'n22', label: 'uses', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e32', graphId: GRAPH_ID, sourceId: 'n02', targetId: 'n25', label: 'related_to', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e33', graphId: GRAPH_ID, sourceId: 'n04', targetId: 'n18', label: 'related_to', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e34', graphId: GRAPH_ID, sourceId: 'n04', targetId: 'n31', label: 'related_to', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e35', graphId: GRAPH_ID, sourceId: 'n19', targetId: 'n01', label: 'depends_on', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e36', graphId: GRAPH_ID, sourceId: 'n19', targetId: 'n20', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e37', graphId: GRAPH_ID, sourceId: 'n23', targetId: 'n24', label: 'includes', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e38', graphId: GRAPH_ID, sourceId: 'n23', targetId: 'n33', label: 'includes', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e39', graphId: GRAPH_ID, sourceId: 'n12', targetId: 'n30', label: 'related_to', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e40', graphId: GRAPH_ID, sourceId: 'n17', targetId: 'n32', label: 'uses', weight: 1.5, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e41', graphId: GRAPH_ID, sourceId: 'n29', targetId: 'n22', label: 'related_to', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
  { id: 'e42', graphId: GRAPH_ID, sourceId: 'n35', targetId: 'n14', label: 'applied_in', weight: 1.0, metadata: null, createdAt: '2026-01-01T00:00:00Z' },
];
