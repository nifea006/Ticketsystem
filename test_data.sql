INSERT INTO users (email, username, first_name, last_name, password, bruker_role, drift_role) VALUES
('ole@example.com', 'olebruker', 'Ole', 'Olsen', '123', TRUE, FALSE),
('kari@example.com', 'karidrift', 'Kari', 'Nordmann', '123', FALSE, TRUE),
('admin@example.com', 'admin', 'Admin', 'User', 'admin', TRUE, TRUE),
('stian@example.com', 'stian', 'Stian', 'Larsen', 'pass', TRUE, FALSE);

INSERT INTO tickets (username, title, description, status) VALUES
('olebruker', 'Internett nede', 'Kan ikke koble til WiFi på PCen.', 'åpen'),
('olebruker', 'Manglende tilgang', 'Jeg får ikke åpnet OneDrive.', 'åpen'),
('karidrift', 'Printer er ødelagt', 'Papirstopp og maskinen slår seg av.', 'under behandling'),
('admin', 'Nettverksfeil', 'Serverrommet har ustabil forbindelse.', 'lukket');