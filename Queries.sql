USE ambulance;
CREATE TABLE IF NOT EXISTS trafficSignals ( id INT AUTO_INCREMENT PRIMARY KEY,
											Lattitude float NOT NULL UNIQUE,
                                            Longitude float NOT NULL UNIQUE,
											Weight_factor float NOT NULL);
                                            
CREATE TABLE IF NOT EXISTS route (  id int auto_increment Primary KEY,
									presentsignalID INT,
									nextsignalID INT,
                                    Foreign KEY (presentsignalID) REFERENCES trafficSignals(id)
                                    ON UPDATE CASCADE ON DELETE CASCADE,
                                    Foreign KEY (nextsignalID) REFERENCES trafficSignals(id)
                                    ON UPDATE CASCADE ON DELETE CASCADE);
                                    
CREATE TABLE IF NOT EXISTS congestion ( SignalID INT NOT NULL,
										TimeOfDay datetime NOT NULL,
                                        avgcongtime INT NOT NULL,
                                        FOREIGN KEY (SignalID) REFERENCES trafficSignals(id) 
                                        ON UPDATE CASCADE ON DELETE CASCADE,
                                        PRIMARY KEY (SignalID,TimeOfDay)
                                        );
CREATE TABLE IF NOT EXISTS ambulanceDetails( Latitude FLOAT NOT NULL,
											 Longitude FLOAT NOT NULL,
											 Name Varchar(50) NOT NULL,
											 Age INT NOT NULL,
											 Dest Text NOT NULL);
                                         
                                         