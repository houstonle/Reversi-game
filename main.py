from reversi import *

def main():
    playAgain = ""
    while playAgain.lower() != 'n':
        # Creating game, choosing colour, and opponent difficulty
        game = Reversi()
        print("Starting new game!\n Black goes first, then white")
        
        while True:
        # Will break when colour is either 'b' or 'w'otherwise continue asking
            try:
                colour = input("Enter 'b' to choose to play black, 'w' to choose white: ")
                assert colour in ['b','w']
                break
            except AssertionError:
                print("Invalid choice. You must pick either 'b' or 'w'")
        game.setPlayerColour(colour)
    
        while True:
        # Will break when difficulty is either 1 or 2 otherwise continue asking.
            try:  
                cpuDiff = input("Enter '1' to choose easy computer opponent, '2' for hard computer opponent: ")
                assert cpuDiff in ['1','2']
                break
            except AssertionError:
                print("Invalid choice. You must pick either '1' or '2'")
        
        # Game set up finished. Start actual gameplay, will only end when there are no more valid moves to be made
        pos = ""
        
        # Case 1: You are black and computer is white
        gameLoop = True
        while gameLoop:
            if colour == 'b':
                # Display initial board with no moves made
                game.displayBoard()
                print("\nScore: white %d, black %d" % (game.getScore("w"), game.getScore("b")))
                # Loop through game for player as black
                while not game.isGameOver() and pos != 'q':
                    print("Enter 2 numbers from 0-7 seperated by a space to make a move,\n where the first number is the row and the second number is the column\nEnter 'q' to quit")
                    
                    # Player move: Keeps looping until valid move is made
                    notValid = True
                    while notValid:
                        pos = input("Enter move: ")
                        # Break out of the loop which asks for move
                        if pos == 'q':
                            break
                        
                        # Check if position are numbers and that they are within the board
                        try:
                            pos = pos.split()
                            pos[0] = int(pos[0])
                            pos[1] = int(pos[1])
                            assert pos[0] in [0,1,2,3,4,5,6,7] and pos[1] in [0,1,2,3,4,5,6,7]
                        except TypeError:
                            print("Must enter numbers from 0-7.")
                        except AssertionError:
                            print("Invalid position: out of bound.")
                        except:
                            print("Please enter 2 numbers from 0-7 seperated by a space.")
                        else:
                            notValid = False
                            
                        # Check that position will result in pieces being changed, thus making it a valid move, if so then make the move.
                        if not notValid:
                            try:
                                assert game.isPositionValid(pos, colour)
                            except AssertionError:
                                if not game.checkEmpty(pos):
                                    print("Invalid position: position is already occupied")
                                else:
                                    print("Invalid position: piece doesn't surround line of opponent\npieces.")
                                notValid = True
                            else:
                                game.makeMovePlayer(pos)
                    
                    # Breaks out of the loop which continues the game. In other words it ends the game
                    if pos == 'q':
                        break
                    
                    game.displayBoard()
                    print("\nScore: white %d, black %d" % (game.getScore("w"), game.getScore("b")))
                    if game.isGameOver() == True:
                        break
                        
                    # Computer move
                    if cpuDiff == '1':
                        game.makeMoveNaive()
                    else:
                        game.makeMoveSmart()
                    game.displayBoard()
                    print("\nScore: white %d, black %d" % (game.getScore("w"), game.getScore("b")))                    
                    game.isGameOver()
                    
            if colour == 'w':
                # Display initial board with no moves made
                game.displayBoard()
                print("\nScore: white %d, black %d" % (game.getScore("w"), game.getScore("b")))
                # Loop through game for player as black
                while not game.isGameOver() and pos != 'q':
                    print("Enter 2 numbers from 0-7 seperated by a space to make a move,\n where the first number is the row and the second number is the column\nEnter 'q' to quit")
                    
                    # Computer move
                    if cpuDiff == '1':
                        game.makeMoveNaive()
                    else:
                        game.makeMoveSmart()
                    game.displayBoard()
                    print("\nScore: white %d, black %d" % (game.getScore("w"), game.getScore("b")))                    
                    if game.isGameOver() == True:
                        break                    
                    
                    # Player move: Keeps looping until valid move is made
                    notValid = True
                    while notValid:
                        pos = input("Enter move: ")
                        if pos == 'q':
                            break
                        
                        # Check if position are numbers and that they are within the board
                        try:
                            pos = pos.split()
                            pos[0] = int(pos[0])
                            pos[1] = int(pos[1])
                            assert pos[0] in [0,1,2,3,4,5,6,7] and pos[1] in [0,1,2,3,4,5,6,7]
                        except TypeError:
                            print("Must enter numbers from 0-7.")
                        except AssertionError:
                            print("Invalid position: out of bound.")
                        except:
                            print("Please enter 2 numbers from 0-7 seperated by a space.")
                        else:
                            notValid = False
                        
                        # Check that position will result in pieces being changed, thus making it a valid move, if so then make the move.   
                        if not notValid:
                            try:
                                assert game.isPositionValid(pos, colour)
                            except AssertionError:
                                if not game.checkEmpty(pos):
                                    print("Invalid position: position is already occupied")
                                else:
                                    print("Invalid position: piece doesn't surround line of opponent\npieces.")
                                notValid = True
                            else:
                                game.makeMovePlayer(pos)
                                
                    if pos == 'q':
                        break
                    game.displayBoard()
                    print("\nScore: white %d, black %d" % (game.getScore("w"), game.getScore("b")))
                    if game.isGameOver() == True:
                        break
                                     
                
            # Checks if player wants to play again. Keeps going until valid input is made.
            while True:
                try:
                    playAgain = input("Do you want to play again (y/n) ?")
                    assert playAgain.lower() in ['y','n']
                except AssertionError:
                    print("Invalid input. Please enter y or n")
                else:
                    break
            # Break out of gameLoop
            break
        
    print("Goodbye!")
                  
main()